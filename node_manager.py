import serial
import serial.tools.list_ports
import threading
import time
import pyudev


class node_manager():
    def __init__(self):
        self.ports = {}
        self.active_threads = {}
        self.stop_event = {}
        self.baudrate = 9600
 

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
                print(f"Adding port: {port.device}")
                print(f"HWID: {port.serial_number}")
                # Fallback to device name if serial number is unavailable
                key = port.serial_number if port.serial_number else port.device
                self.ports[key] = port
            
                

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

            # Continuously read from the serial port
            while not stop_event.is_set(): 
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    print(f"Data from {port.serial_number}: {line}")

        except Exception as e:
            print(f"Error with {device}: {e}")
        finally:
            # Ensure we close the serial connection properly
            if 'ser' in locals() and ser.is_open:
                print(f"Closing connection to {device}")
                ser.close()
                
    def get_database_connection(self):
        
        

# Define the main function
def main():
    # Create an instance of node_manager
    p = node_manager()
    p.get_ports()
    p.connect_nodes()

    try:
        # Keep the main program running, so the threads don't exit
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        for device, stop_event in p.stop_event.items():
            stop_event.set()  # Signal all threads to stop


# Run the main program
if __name__ == "__main__":
    main()
