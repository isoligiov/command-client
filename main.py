import websocket
import ssl
import rel
import json
import time

SERVER_URL = 'http://streamlineanalytics.net:10000'

ws = None

def send_command(ws, data):
    encoded_data = json.dumps(data).encode('utf-8')
    ws.send_text(encoded_data)

def on_message(ws, message):
    pass

def on_error(ws, error):
    print(error)
    time.sleep(2)
    reconnect()

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    time.sleep(2)
    reconnect()

def on_open(ws):
    print("Opened connection\n")
    app_name = None
    while True:
        app_name = input('app name: ').strip()
        if len(app_name) == 0:
            print('Invalid app name')
            exit(0)
        break

    while True:
        command = input('command: ').strip()
        if len(command) == 0:
            print('Invalid command')
            exit(0)
        data = { 'type': 'cmd', 'room': app_name, 'command': command }
        send_command(ws, data)
        print('sent\n')

def reconnect():
    global ws
    ws = websocket.WebSocketApp(f"wss://streamlineanalytics.net:10001",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, dispatcher=rel, reconnect=5)

if __name__ == "__main__":
    websocket.enableTrace(False)
    reconnect()
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
