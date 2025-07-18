import requests

TEST_USERNAME1 = 'ostiness'
TEST_PASS1 = 'Iness567'
TEST_USERNAME2 ='ostiness2'
TEST_PASS2='Iness567'
BASE_URL = 'http://localhost:8000/api'

def register(username,passwd):
    response = requests.post(F'{BASE_URL}/auth/registration/',data={
        'username':username,
        'password1':passwd,
        'password2':passwd
    })
    if response.ok:
        return response.json()['key']
    print('registration response:',response.content)

register(TEST_USERNAME1,TEST_PASS1)
register(TEST_USERNAME2,TEST_PASS2)
def login(username,passwd):
    res=requests.post(f'{BASE_URL}/auth/login',data={
        'username':username,
        'password':passwd
    })
    if res.ok:
        return res.json()['key']
    print('login error:',res.content)

class Client:
    def __init__(self,username,password) -> None:
        key = login(username,password)
        self.username = username
        self.headers={'Authorization':f'Token {key}'}

    def create_phonebook(self,name,**attrs):
        attrs['name']=name
        response = requests.post(f'{BASE_URL}/phonebooks/',headers=self.headers,data=attrs)
        print(self.username,'created phonebook',response.json())

    def list_phonebooks(self):
        response = requests.get(f'{BASE_URL}/phonebooks/',headers=self.headers)
        print(self.username,'listing phonebooks',response.json())


    def create_column(self,name,phonebook):
        response = requests.post(f'{BASE_URL}/columns/',headers=self.headers,data={
            'name':name,
            'phonebook':phonebook
        })
        print(self.username,'creating column',response.json())

    def create_contact(self,name,phone,phonebook):
        response = requests.post(f'{BASE_URL}/phonebooks/{phonebook}/contacts/',headers=self.headers,data={
            'name':name,
            'phone':phone,
        })
        print(self.username,'creating contact',response.json())

    def create_attribute(self,contact,column,value):
        response = requests.post(f'{BASE_URL}/attributes/',headers=self.headers,data={
            'contact':contact,
            'column':column,
            'value':value
        })
        print(self.username,'creaing attribute',response.json())
    def list_contacts(self):
        res=requests.get(f'{BASE_URL}/phonebooks/1/contacts/',headers=self.headers,)
        print(self.username,'listing contacts',res.json())

client1 = Client(TEST_USERNAME1,TEST_PASS1)
client1.create_phonebook('new phonebook')
client1.create_column('ability',1)
client1.create_contact('kevin','0712344567',1)
client1.create_attribute(1,1,100)
client1.list_contacts()
client1 = Client(TEST_USERNAME2,TEST_PASS1)
client1.create_phonebook('phonebook2')
client1.create_column('ability',1)
client1.create_contact('eliud','0732344567',1)
client1.create_attribute(1,1,100)
client1.list_contacts()
client1.list_phonebooks()