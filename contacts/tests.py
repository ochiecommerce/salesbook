from rest_framework.test import APIClient, APITestCase


class PhonebookTest(APITestCase):
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

    def test_create_phonebook(self):
        response = self.client.post(
            "/api/phonebooks/",
            data={"name": "phonebook1", "description": "my first phonebook"},
            headers=self.client.headers,
        )
        assert 'name' in response.json().keys()

    def test_create_contact(self):
        response = self.client.post(
            "/api/phonebooks/",
            data={"name": "phonebook1", "description": "my first phonebook"},
            headers=self.client.headers,
        )
        phonebook=response.json()
        response = self.client.post(
            f"/api/phonebooks/{phonebook['pk']}/contacts/",
            data={"name":'kevin otieno','phone':'0771234567'},
            headers=self.client.headers,
        )
        assert 'name' in response.json().keys()