from rest_framework.test import APIClient, APITestCase


class MessageTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client.post(
            "/api/user/registration/",
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        response = self.client.post(
            "/api/user/login/", {"username": "testuser", "password": "testpassword"}
        )
        token = response.json()["key"]
        self.client.headers = {"Authorization": f"Token {token}"}
        return super().setUp()

    def test_get_messages(self):
        response = self.client.get("/api/forum/messages/", headers=self.client.headers)
        assert type(response.json())==list

    def test_create_messages(self):
        message = {"message": "how to create a market?"}
        response = self.client.post(
            "/api/forum/messages/", headers=self.client.headers, data=message
        )
        assert 'message' in response.json().keys()
        
        self.test_get_messages()

