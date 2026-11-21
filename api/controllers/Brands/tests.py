import uuid

from django.test import SimpleTestCase
from django.urls import resolve


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
