import requests
import json

URL  = 'http://127.0.0.1:11434/api/generate'

res=requests.post(url=URL,json={'model':'deepseek-coder','prompt':'how to write vscode extension'},stream=True)

for line in res.iter_lines(decode_unicode=True):
    response = json.loads(line)
    print(response['response'])

