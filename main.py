from websockets.sync.client import connect
import ssl
import json
import time

websocket_server_url = "wss://streamlineanalytics.net:10001"

def send_command(ws, data):
    encoded_data = json.dumps(data).encode('utf-8')
    ws.send(encoded_data)


if __name__ == "__main__":
    app_name = None
    while True:
        app_name = input('app name: ').strip()
        if len(app_name) == 0:
            print('Invalid app name')
            exit(0)
        break

    while True:
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            with connect(websocket_server_url, ssl=ssl_context) as ws:
                print('Opened connection')

                while True:
                    command = input('command: ').strip()
                    if len(command) == 0:
                        print('Invalid command')
                        exit(0)
                    data = { 'type': 'cmd', 'room': app_name, 'command': command }
                    send_command(ws, data)
                    print('sent\n')

        except Exception as e:
            print('ERR', e)
        time.sleep(5)