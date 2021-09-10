import requests
import json 

def http_request(url, text):
    payload = {'text': str(text)}
    requests.post(url, data=json.dumps(payload))
