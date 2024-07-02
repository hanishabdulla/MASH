import serial
import serial.tools.list_ports
import time

try:
    arduino = serial.Serial('/dev/tty.usbmodem1401', 9600, timeout=1)
    print("Connected to Arduino")

    while True:
        if arduino.in_waiting:
            message = arduino.readline().decode('utf-8').rstrip()
            if message == "OMG":  # Changed to match the Arduino's output
                print("omg")  # You can change this to print "OMG" if you prefer
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"Error: {e}")
    print("Make sure Arduino is connected and no other program is using the port.")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    if 'arduino' in locals():
        arduino.close()