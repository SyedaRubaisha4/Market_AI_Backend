import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import resolve
from rest_framework.test import APIRequestFactory, force_authenticate

from api.controllers.Brands.views import view_create_brand, view_update_brand


class BrandUrlTests(SimpleTestCase):
    def test_brand_routes_accept_uuid_primary_keys(self):
        brand_id = uuid.uuid4()
        routes = (
            (f"/api/brands/{brand_id}/", "get_brand"),
            (f"/api/brands/{brand_id}/update/", "update_brand"),
            (f"/api/brands/{brand_id}/delete/", "delete_brand"),
        )

        for path, url_name in routes:
            with self.subTest(path=path):
                match = resolve(path)
                self.assertEqual(match.url_name, url_name)
                self.assertEqual(match.kwargs["brand_id"], brand_id)


class BrandCreateResponseTests(SimpleTestCase):
    def test_create_returns_complete_saved_brand(self):
        user = SimpleNamespace(id=uuid.uuid4(), is_authenticated=True)
        brand = SimpleNamespace(
            id=uuid.uuid4(),
            created_on=datetime(2026, 1, 1, tzinfo=timezone.utc),
            updated_on=datetime(2026, 1, 2, tzinfo=timezone.utc),
            action_type=1,
            user=user,
            business_name="Example Brand",
            business_type="Retail",
            description="An example brand",
            tone_of_voice=["Friendly"],
            target_customer_class="middle",
            customer_type="women",
            language="English",
            words_to_avoid=["cheap"],
            brand_keywords=["quality"],
            status="Active",
        )
        request = APIRequestFactory().post(
            "/api/brands/create/",
            {"business_name": brand.business_name},
            format="json",
        )
        force_authenticate(request, user=user)

        with patch(
            "api.controllers.Brands.views.create_brand",
            return_value=brand,
        ):
            response = view_create_brand(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["id"], brand.id)
        data = response.data["data"]
        self.assertEqual(
            set(data),
            {
                "id",
                "created_on",
                "updated_on",
                "action_type",
                "user_id",
                "business_name",
                "business_type",
                "description",
                "tone_of_voice",
                "target_customer_class",
                "customer_type",
                "language",
                "words_to_avoid",
                "brand_keywords",
                "status",
            },
        )
        self.assertEqual(data["id"], str(brand.id))
        self.assertEqual(data["user_id"], str(user.id))
        self.assertEqual(data["business_name"], brand.business_name)
        self.assertEqual(data["tone_of_voice"], brand.tone_of_voice)


class BrandUpdateAuthenticationTests(SimpleTestCase):
    def test_update_requires_authentication(self):
        brand_id = uuid.uuid4()
        request = APIRequestFactory().patch(
            f"/api/brands/{brand_id}/update/",
            {"description": "Updated description"},
            format="json",
        )

        with patch("api.controllers.Brands.views.update_brand") as update:
            response = view_update_brand(request, brand_id)

        self.assertEqual(response.status_code, 401)
        update.assert_not_called()

    def test_authenticated_user_can_update_brand(self):
        user = SimpleNamespace(id=uuid.uuid4(), is_authenticated=True)
        brand_id = uuid.uuid4()
        request = APIRequestFactory().patch(
            f"/api/brands/{brand_id}/update/",
            {"description": "Updated description"},
            format="json",
        )
        force_authenticate(request, user=user)

        with patch("api.controllers.Brands.views.update_brand") as update:
            response = view_update_brand(request, brand_id)

        self.assertEqual(response.status_code, 200)
        update.assert_called_once_with(
            user, brand_id, {"description": "Updated description"}
        )
