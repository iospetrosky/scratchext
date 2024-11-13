import serial
ser = serial.Serial("COM11",115200,timeout=1)

while True:
    c = ser.read(1024).decode('UTF-8')
    print(c)