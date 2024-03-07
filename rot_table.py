import requests

api_addr = "http:/192.168.1.10:8081/api/"
str_json_request = ".json?"

def send_command(command="getConfig"):
    out = requests.get(f"{api_addr}{command}{str_json_request}")
    print(out.json())

def send_pos(pitch, yaw, command="executaPosicionamento"):
    out = requests.get(f"{api_addr}{command}{str_json_request}posAzimute={yaw}&posTilt={pitch}")
    print(out.json())

def send_vel(pitch, yaw, command="executaJog"):
    if pitch == 0 & yaw == 0:
        stop()
    out = requests.get(f"{api_addr}{command}{str_json_request}velAzimute={yaw}&velTilt={pitch}")
    print(out.json())

def stop():
    out = requests.get(f"{api_addr}executaParar{str_json_request}")
    print(out.json())

def get_state():
    out = send_command(dados)
    print(out.json())
