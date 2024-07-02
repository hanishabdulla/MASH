import os
import cv2
import threading
import serial.tools.list_ports
import serial
from google.cloud import vision
from google.cloud.vision_v1 import types

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"Google Cloud API Keys.json"

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    result = []
    for port in ports:
        result.append((port.device, port.description, port.manufacturer))
    return result

def process_image(serialInst):
    try:
        value = "data_to_send"
        serialInst.write(value.encode('utf-8'))
    except serial.SerialException as e:
        print(f"Serial write error: {e}")

def main():
    ports = list_serial_ports()
    
    print("Available serial ports:")
    for i, (device, description, manufacturer) in enumerate(ports):
        print(f"{i + 1}: {device} - {description} - {manufacturer}")

    if not ports:
        print("No serial ports found.")
        return
    
    try:
        selected_port_index = int(input("Select microcontroller port: ")) - 1
        if selected_port_index < 0 or selected_port_index >= len(ports):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_port = ports[selected_port_index][0]
    print(f"Selected port: {selected_port}")

    # Example: Open the selected serial port
    try:
        ser = serial.Serial(selected_port, 9600, timeout=1)
        print(f"Connected to {selected_port}")

        # Initialize Google Cloud Vision client
        client = vision.ImageAnnotatorClient()

        # Start a thread to process image and send data to serial port
        thread = threading.Thread(target=process_image, args=(ser,))
        thread.start()
        thread.join()

        ser.close()
    except serial.SerialException as e:
        print(f"Error opening serial port {selected_port}: {e}")

if __name__ == "__main__":
    main()
