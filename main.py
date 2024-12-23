import websocket
import ssl
import rel
import json
import time
import threading

SERVER_URL = 'http://streamlineanalytics.net:10000'

ws = None

def send_command(data):
    global ws
    encoded_data = json.dumps(data).encode('utf-8')
    try:
        ws.send_text(encoded_data)
    except:
        print('Error while sending command')

def on_message(ws, message):
    pass

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(_ws):
    global ws
    print("Opened connection\n")
    ws = _ws

def input_thread():
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
        send_command(data)
        print('sent\n')

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"wss://streamlineanalytics.net:10001",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, dispatcher=rel, reconnect=5, ping_interval=10, ping_timeout=9)

    input_handler = threading.Thread(target=input_thread)
    input_handler.start()

    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
