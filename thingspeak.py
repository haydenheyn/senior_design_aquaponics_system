import requests
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")



thingspeak_api_write_key = config["thingspeak"]["writeapikey"]
value = 1
url = f"https://api.thingspeak.com/update?api_key={thingspeak_api_write_key}&field1={value}"
response = requests.get(url)