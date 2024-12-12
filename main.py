import urllib.request
import urllib.parse
import sys
import json

SERVER_URL = 'http://5.133.9.244:10000'

def send_post_request(url, data):
    encoded_data = json.dumps(data).encode('utf-8')
    request = urllib.request.Request(url, data=encoded_data, method='POST')
    request.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(request) as response:
        response_data = response.read().decode('utf-8')
    return response_data

app_name = None
command = None
if len(sys.argv) < 2:
    app_name = input('app name: ').strip()
else:
    app_name = sys.argv[1]

if len(sys.argv) < 3:
    command = input('command: ').strip()
else:
    command = sys.argv[2]


url = f'{SERVER_URL}/cmd'
data = {
    'text': f'{app_name} {command}'
}

response = send_post_request(url, data)
print(response)