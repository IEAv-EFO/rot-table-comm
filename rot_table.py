# Set of API functions to control IEAv rotary table.
# 
# The server has to be running in any computer connected to the table network switch
# the api_addr is the address and port of this server.


import requests

def config_address(ip="192.168.1.10", port="8081"):
    api_addr = f"http://{ip}:{port}/api/"
    str_json_request = ".json?"
    return api_addr, str_json_request

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
    out = send_command("dados")
    print(out.json())

api_addr, str_json_request = config_address()