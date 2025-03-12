import time 
import board 
import busio 
import digitalio 
import requests
from configparser import ConfigParser
from adafruit_bme280 import basic as adafruit_bme280 

config = ConfigParser()
config.read("config.ini")


thingspeak_api_write_key = config["thingspeak"]["writeapikey"]
 

# Create the SPI interface 
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO) 
# Create the CS (Chip Select) pin 
cs = digitalio.DigitalInOut(board.D5)  # Using GPIO 5 as CS pin 
# Create the BME280 sensor object 
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs) 


 

def read_sensor(): 
    temperature = bme280.temperature*9/5 + 32 
    humidity = bme280.relative_humidity 
    url = f"https://api.thingspeak.com/update?api_key={thingspeak_api_write_key}&field1={temperature}&field2={humidity}"
    response = requests.get(url)
    #url = f"https://api.thingspeak.com/update?api_key={thingspeak_api_write_key}&field1={temperature}"
    #response = requests.get(url)
    print(f"Temperature: {temperature:.2f} °F") 
    print(f"Humidity: {humidity:.2f} %") 
    print(response)
    return temperature, humidity 

 

if __name__ == "__main__": 
    # First reading might be inaccurate, so discard it 
    read_sensor() 
    print("BME280 Continuous Reading Mode - Press CTRL+C to exit") 
    try: 
        while True: 
            read_sensor() 
            time.sleep(600)  # Read every 2 seconds 
            print("------------------------") 
    except KeyboardInterrupt: 
        print("Program ended by user") 
