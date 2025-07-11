import requests

res=requests.post('http://localhost:8000/contacts/api/auth/login',data={
    'username':'ostiness',
    'password':'Vevorahh'
})

if not res.ok:
    print(res.content)
    exit()

token = res.json()['key']
print('Token',token)
def list_contacts():
    res=requests.get('http://localhost:8000/contacts/api/contacts/',headers={'Authorization':f'Token {token}'},)
    print(res.content)

list_contacts()