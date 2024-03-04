
import requests

api_addr = "http://127.0.0.1:8088/api/"
str_json_request = ".json?"

def send_command(command="getConfig"):
    out = requests.get(api_addr + command + str_json_request)
    print(out.json())

def set_pos(pitch, yaw, command="executaPosicionamento"):
    out = requests.get(api_addr + command + str_json_request + "posAzimute=" + str(yaw) + "&posTilt=" + str(pitch))
    print(out.json())

def set_vel(pitch, yaw, command="executaJog"):
    if pitch == 0 & yaw == 0:
        stop()
    out = requests.get(api_addr + command + str_json_request + "velAzimute=" + str(yaw) + "&velTilt=" + str(pitch))
    print(out.json())

def stop():
    out = requests.get("http://127.0.0.1:8088/api/executaParar.json?")
    print(out.json())


send_command()
set_pos(0, 0)
set_vel(0, 0)