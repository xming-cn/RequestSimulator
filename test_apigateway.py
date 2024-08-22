import json
import requests
from objprint import op

url = 'https://y2ud2sq4x6.execute-api.us-east-2.amazonaws.com/v1'
response = requests.get(url)

# for attr in dir(response):
    # print(f'{attr}: ', end='')
    # op(getattr(response, attr))

res_json = json.loads(response.content)
op(res_json)
# op(json.loads(res_json['body']))