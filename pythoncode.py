"""
    Program to read data from Novafitness SDS011
    http://aqicn.org/sensor/sds011/
    
    Original program by
    Nils Jacob Berland
    njberland@gmail.com / njberland@sensar.io
    +47 40800410
    
    Modified by
    Szymon Jakubiak

    Measured values of PM2.5 and PM10 are in ug/m^3
"""
import serial

# Specify serial port address
ser_port = "COM11"

ser = serial.Serial(ser_port, baudrate=9600, stopbits=1, parity="N",  timeout=2)

try:
    while True:
        ser.flushInput()
        s = ser.read(2)
        # Check if data header is correct
        if s[0] == int("AA",16) and s[1] == int("C0",16):
            s = ser.read(8)
            pm25_lb= s[0]   # low byte
            pm25_hb= s[1]   # high byte
            pm10_lb= s[2]
            pm10_hb= s[3]
            cs = s[6]   # check sum
            tail = s[7]
            # Check if data tail is correct
            if s[7] == int("AB",16):
                # Calculate check sum vale
                check = (s[0] + s[1] + s[2] + s[3] + s[4] + s[5]) % 256
                # # Check if check sum is correct
                if check == cs:
                    try:
                        # Sensor unique ID
                        sensor_id = hex(s[4])[-2:] + hex(s[5])[-2:]
                        pm25 = float(pm25_hb * 256 + pm25_lb) / 10.0
                        pm10 = float(pm10_hb * 256 + pm10_lb) / 10.0
                        print("ID:", sensor_id, " PM2.5:", pm25, "ug/m^3  PM10:", pm10, "ug/m^3")
                    except:
                        pass
except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")
