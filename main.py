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
while True:
    app_name = input('app name: ').strip()
    if len(app_name) == 0:
        print('Invalid app name')
        continue
    break

while True:
    command = input('command: ').strip()
    if len(command) == 0:
        print('Invalid command')
        continue
    url = f'{SERVER_URL}/cmd'
    data = { 'text': f'{app_name} {command}' }
    response = send_post_request(url, data)
    print('sent')
    print()