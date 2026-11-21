from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory

from api.controllers.Auth.views import view_register_user


class RegisterUserViewTests(SimpleTestCase):
    def test_duplicate_username_error_is_readable(self):
        request = APIRequestFactory().post(
            "/api/auth/register/",
            {
                "username": "existing-user",
                "email": "new@example.com",
                "password": "ValidPassword123!",
            },
            format="json",
        )
        with patch(
            "api.controllers.Auth.views.register_user",
            side_effect=ValidationError(
                "Username already taken. Please choose a different username or log in."
            ),
        ):
            response = view_register_user(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "success": False,
                "errors": (
                    "Username already taken. Please choose a different username or log in."
                ),
            },
        )
