import requests

def prrint(*args):
    print(*args)
    return args[0]

TEST_USERNAME1 = "ostiness"
TEST_PASS1 = "Iness567"
TEST_USERNAME2 = "ostiness2"
TEST_PASS2 = "Iness567"
BASE_URL = "http://localhost:8000/api"


def register(username, passwd):
    response = requests.post(
        f"{BASE_URL}/auth/registration/",
        data={"username": username, "password1": passwd, "password2": passwd},
    )
    if response.ok:
        return response.json()["key"]
    print("registration response:", response.content)


register(TEST_USERNAME1, TEST_PASS1)
register(TEST_USERNAME2, TEST_PASS2)


def login(username, passwd):
    res = requests.post(
        f"{BASE_URL}/auth/login", data={"username": username, "password": passwd}
    )
    if res.ok:
        ret=res.json()
        print(ret)
        return ret['key']
    print("login error:", res.content)


class Client:
    def __init__(self, username, password) -> None:
        key = login(username, password)
        self.username = username
        self.headers = {"Authorization": f"Token {key}"}

    @property
    def user(self):
        response = requests.get(f"{BASE_URL}/auth/user/", headers=self.headers)
        if response.ok:
            return prrint(response.json())
        print(self.username, "getting user info", response.json())

    def create_phonebook(self, name, **attrs):
        attrs["name"] = name
        response = requests.post(
            f"{BASE_URL}/phonebooks/", headers=self.headers, data=attrs
        )
        if response.ok:
            return response.json()
        print(self.username, "creating phonebook", response.json())

    def list_phonebooks(self):
        response = requests.get(f"{BASE_URL}/phonebooks/", headers=self.headers)
        if response.ok:
            return response.json()
        print(self.username, "listing phonebooks", response.json())

    def create_column(self, name, phonebook):
        response = requests.post(
            f"{BASE_URL}/columns/",
            headers=self.headers,
            data={"name": name, "phonebook": phonebook},
        )
        print(self.username, "creating column", response.json())

    def add_read_permission(self, phonebook,user):
        response = requests.post(
            f"{BASE_URL}/phonebooks/{phonebook}/read_permissions/",
            headers=self.headers,
            data={"user": user},
        )
        if response.ok:
            return response.json()
        print(self.username, "adding read permission", response.json())

    def add_write_permission(self, phonebook,user):
        response = requests.post(
            f"{BASE_URL}/phonebooks/{phonebook}/write_permissions/",
            headers=self.headers,
            data={"user": user},
        )
        if response.ok:
            return response.json()
        print(self.username, "adding write permission", response.json())

    def add_alter_permission(self, phonebook,user):
        response = requests.post(
            f"{BASE_URL}/phonebooks/{phonebook}/alter_permissions/",
            headers=self.headers,
            data={"user": user},
        )
        if response.ok:
            return response.json()
        print(self.username, "adding alter permission", response.json())
    
    def list_permissions(self, phonebook):
        response = requests.get(
            f"{BASE_URL}/phonebooks/{phonebook}/read_permissions/",
            headers=self.headers,
        )
        if response.ok:
            return response.json()
        print(self.username, "listing permissions", response.json())

    def list_write_permissions(self, phonebook):
        response = requests.get(
            f"{BASE_URL}/phonebooks/{phonebook}/write_permissions/",
            headers=self.headers,
        )
        if response.ok:
            return response.json()
        print(self.username, "listing write permissions", response.json())

    def list_alter_permissions(self, phonebook):
        response = requests.get(
            f"{BASE_URL}/phonebooks/{phonebook}/alter_permissions/",
            headers=self.headers,
        )
        if response.ok:
            return response.json()
        print(self.username, "listing alter permissions", response.json())
    def create_contact(self, name, phone, phonebook):
        response = requests.post(
            f"{BASE_URL}/phonebooks/{phonebook}/contacts/",
            headers=self.headers,
            data={
                "name": name,
                "phone": phone,
            },
        )
        if response.ok:
            return response.json()
        print(self.username, "creating contact", response.json())

    def create_attribute(self, contact, column, value):
        response = requests.post(
            f"{BASE_URL}/attributes/",
            headers=self.headers,
            data={"contact": contact, "column": column, "value": value},
        )
        if response.ok:
            return response.json()
        print(self.username, "creating attribute", response.json())

    def list_contacts(self):
        res = requests.get(
            f"{BASE_URL}/phonebooks/1/contacts/",
            headers=self.headers,
        )
        if res.ok:
            return res.json()
        print(self.username, "listing contacts", res.json())

    def create_note(self, title, note):
        res = requests.post(
            f"{BASE_URL}/notes/",
            headers=self.headers,
            data={"title": title, "note": note},
        )
        if res.ok:
            return res.json()
        print(self.username, "creating note", res.json())

    def list_notes(self):
        res = requests.get(
            f'{BASE_URL}/notes',
            headers=self.headers
        )
        if res.ok:
            return res.json()
        print(self.username, "listing notes", res.json())


client1 = Client(TEST_USERNAME1, TEST_PASS1)
client2 = Client(TEST_USERNAME2, TEST_PASS1)
phonebook1=client1.create_phonebook("new phonebook")
print(client1.list_permissions(phonebook1["pk"]))
print(client2.list_phonebooks())
client1.add_read_permission(phonebook1["pk"], client2.user["pk"])
print(client1.username,'listing permissions',client1.list_permissions(phonebook1['pk']))
print(client2.list_permissions(phonebook1["pk"]))

print(client2.list_phonebooks())
client1.create_column("ability", phonebook1['pk']) # type: ignore
client1.create_contact("kevin", "0712344567", phonebook1["pk"])
client1.create_attribute(1, 1, 100)
client1.list_contacts()
client2.create_contact("eliud", "0732344567", phonebook1["pk"])
client1.add_write_permission(phonebook1["pk"], client2.user["pk"])
client2.create_contact("eliud", "0732344567", phonebook1["pk"])
client2.create_note("Meeting", "attending a meeting at noon @contacts/0732344567")
client2.create_column("ability", 1)
client2.create_attribute(1, 1, 100)
client2.list_contacts()
phonebooks2=client2.list_phonebooks()
print("Phonebooks for client2:", phonebooks2)
client2.list_notes()