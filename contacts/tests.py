from pyparsing import col
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
        phonebook: dict = response.json()
        assert "name" in phonebook.keys()
        return phonebook

    def test_create_contact(self):
        phonebook = self.test_create_phonebook()
        response = self.client.post(
            f"/api/phonebooks/{phonebook['pk']}/contacts/",
            data={"name": "kevin otieno", "phone": "0771234567"},
            headers=self.client.headers,
        )
        contact: dict = response.json()
        assert "name" in contact.keys()
        return contact

    def test_list_phonebooks(self):
        self.test_create_phonebook()
        response = self.client.get("/api/phonebooks/", headers=self.client.headers)
        phonebooks: list = response.json()
        assert len(phonebooks) > 0
        return phonebooks

    def test_create_column(self):
        phonebook = self.test_create_phonebook()
        response = self.client.post(
            "/api/columns/",
            data={"name": "column1", "phonebook": phonebook["pk"]},
            headers=self.client.headers,
        )
        column: dict = response.json()
        assert "name" in column.keys()
        return column

    def test_list_contacts(self):
        phonebook = self.test_create_phonebook()
        self.test_create_column()
        self.test_create_contact()
        response = self.client.get("/api/phonebooks")
