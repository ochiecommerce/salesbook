import requests

URL  = 'http://127.0.0.1:11434/api/generate'

res=requests.post(url=URL,data={'model':'deepseek-coder'})
print(res.json())