import psycopg2
from configparser import ConfigParser
import time
import board 
import busio 
import digitalio 
from adafruit_bme280 import basic as adafruit_bme280


# Create the SPI interface 
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO) 
# Create the CS (Chip Select) pin 
cs = digitalio.DigitalInOut(board.D5)  # Using GPIO 5 as CS pin 
# Create the BME280 sensor object 
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)  
config = ConfigParser()
config.read("config.ini")

def read_sensor(): 
    temperature = bme280.temperature*9/5 + 32 
    humidity = bme280.relative_humidity 
    print(f"Temperature: {temperature:.2f} °F") 
    print(f"Humidity: {humidity:.2f} %") 
    return temperature, humidity 

# Use the actual IP address of the server and the database credentials
db_host = config["database"]["host"]  
db_name = config["database"]["name"]
db_user = config["database"]["user"]
db_password = config["database"]["password"]

try:
    # Establish connection
    connection = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    print("Connection successful!")
       
except Exception as e:
    print("Error:", e)


if __name__ == "__main__": 
    # First reading might be inaccurate, so discard it 
    read_sensor() 
    print("BME280 Continuous Reading Mode - Press CTRL+C to exit") 
    try: 
        while True: 	
            read_sensor() 
            time.sleep(200)  # Read every 2 seconds 
            print("------------------------") 
    except KeyboardInterrupt: 
        print("Program ended by user") 

















finally:
    if connection:
        connection.close()
