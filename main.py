from websockets.sync.client import connect
import json
import time

websocket_server_url = "ws://5.133.9.244:10010"

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
            with connect(websocket_server_url) as ws:
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