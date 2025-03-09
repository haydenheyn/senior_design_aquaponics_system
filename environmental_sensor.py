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

 

def read_sensor(): 
    temperature = bme280.temperature 
    humidity = bme280.relative_humidity 
    print(f"Temperature: {temperature:.2f} °C") 
    print(f"Humidity: {humidity:.2f} %") 
    return temperature, humidity 

 

if __name__ == "__main__": 
    # First reading might be inaccurate, so discard it 
    read_sensor() 
    print("BME280 Continuous Reading Mode - Press CTRL+C to exit") 
    try: 
        while True: 
            read_sensor() 
            time.sleep(2)  # Read every 2 seconds 
            print("------------------------") 
    except KeyboardInterrupt: 
        print("Program ended by user") 
