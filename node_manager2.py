import serial
import serial.tools.list_ports
import threading
import time
import pyudev
import requests
from configparser import ConfigParser



class node_manager():
    def __init__(self):
        self.ports = {}
        self.active_threads = {}
        self.stop_event = {}
        self.baudrate = 115200
 

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
                print(f"Adding port: {port.device}")
                print(f"HWID: {port.serial_number}")
                # Fallback to device name if serial number is unavailable
                key = port.serial_number if port.serial_number else port.device
                self.ports[key] = port
                
    def writeAPI(self, temperature_0,temperature_1,tds_1,tds_2 ,oxygen_1 ,ph_1 ,ph_2 ,distance_1 ,distance_2 , serial):
            #Require asynch function
            #Parse Line
            # Arduino 1 = channel2
            if serial == "F412FA9C96E0":
                apikey = "8LI3STSLW9DY9EEJ"            
                url = f"https://api.thingspeak.com/update?api_key={apikey}&field1={temperature_0}&field2={temperature_1}&field3={tds_1}&field4={tds_2}&field5={ph_1}&field6={ph_2}&field7={distance_1}&field8={distance_2}"
            response = requests.get(url)       
                

    def connect_nodes(self):
        for key in self.ports:
            port = self.ports[key] 
            self.connect_device(port)

    def connect_device(self, port):
        stop_event = threading.Event()
        self.stop_event[port.device] = stop_event
        thread = threading.Thread(target=self.handle_connection, args=(port, stop_event))
        thread.start()

        # Store the active thread using the device name or serial number as a key
        self.active_threads[port.device] = thread
        print(f"Started thread for {port.device}")

    def handle_connection(self, port, stop_event):
        try:
            device = port.device  # Get the device name
            # Initialize the serial connection
            ser = serial.Serial(device, self.baudrate, timeout=1)
            ser.reset_input_buffer()
            print(f"Connected to {device}")
            
            # Values that will read into the system
            temperature_0 = 0.0
            temperature_1 = 0.0
            tds_1 = 0
            tds_2 = 0
            oxygen_1 = 0
            ph_1 = 0.0
            ph_2 = 0.0
            distance_1 = 0.0
            distance_2 = 0.0
            
            # Read 8 Lines
            linecount = 0
            # Continuously read from the serial port
            while not stop_event.is_set(): 
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    print(f"Data from {port.serial_number}: {line}")
                    ls = line.split(":")
                    if (ls[0] == "Temperature 0"):
                       temperature_0 = float(ls[1].strip())
                        
                    elif (ls[0] == "Temperature 1"):
                       temperature_1 = float(ls[1].strip())
                        
                    elif (ls[0] == "TDS 1"):
                       tds_1 = int(ls[1].strip())
                        
                    elif (ls[0] == "TDS 2"):
                       tds_2 = int(ls[1].strip())
                        
                    elif (ls[0] == "PH 1"):
                        ph_1 = float(ls[1].strip())
                        
                    elif (ls[0] == "PH 2"):
                        ph_2 = float(ls[1].strip())
                        
                    elif (ls[0] == "Distance 1"):
                        distance_1 = float(ls[1].strip())
                        
                    elif (ls[0] == "Distance 2"):
                        distance_2 = float(ls[1].strip())
                    elif (ls[0] == "error"):
                        print("error")
                        
                    if linecount == 8:
                        self.writeAPI(temperature_0,temperature_1,tds_1,tds_2 ,oxygen_1 ,ph_1 ,ph_2 ,distance_1 ,distance_2 ,port.serial_number)
                    else: linecount += 1
                        
                        
                    
        except Exception as e:
            print(f"Error with {device}: {e}")
        finally:
            # Ensure we close the serial connection properly
            if 'ser' in locals() and ser.is_open:
                print(f"Closing connection to {device}")
                ser.close()
                
        
                
                
""" 
                    INPUT DATA FORMAT
        Data from F412FA9C96E0: Temperature 0: 66.76 F
        Data from F412FA9C96E0: Temperature 1: 70.25 F
        Data from F412FA9C96E0: TDS 1: 1001 ppm
        Data from F412FA9C96E0: TDS 2: 0 ppm
        Data from F412FA9C96E0: Oxgyen 1: 113
        Data from F412FA9C96E0: PH 1: 12.00
        Data from F412FA9C96E0: PH 2: 12.00
        Data from F412FA9C96E0: Distance 1: 5.52 cm
        Data from F412FA9C96E0: Distance 2: 3.94 cm
""" 
    
                

        
    
        
        

# Define the main function
def main():
    
    config = ConfigParser()
    config.read("config.ini")
    thingspeak_api_write_key = config["thingspeak"]["writeapikey"]
    thingspeak_api_write_key_channel_2 = config["thingspeak"]["writeapiekey2_channel_2"]
    
   
   
    # Create an instance of node_manager
    p = node_manager()
    p.get_ports()
    p.connect_nodes()

    try:
        # Keep the main program running, so the threads don't exit
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down gracefully...s")
        for device, stop_event in p.stop_event.items():
            stop_event.set()  # Signal all threads to stop


# Run the main program
if __name__ == "__main__":
    main()
