
import serial.tools.list_ports
import serial
import time
from datetime import datetime, timedelta
ports = serial.tools.list_ports.comports()



serialInst = serial.Serial()
portsList=[]

for i in ports: 
    portsList.append(str(i))
ports = serial.tools.list_ports.comports()

serialInst = serial.Serial()
portsList=[]

for i in ports: 
    portsList.append(str(i))
    print(i)
com=input("select micro-controller port: ")



serialInst.baudrate= 9600
serialInst.port= '/dev/tty.usbmodem11101'
serialInst.open()

serialInst.write("LHRHUB".encode('utf-8'))

if __name__ == "__main__":
    main()
    print(i)
com=input("select micro-controller port: ")
