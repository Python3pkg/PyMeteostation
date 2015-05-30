#!/usr/bin/python

import os
import time
import datetime
import sys
import serial

sys.stdout.write("WS981 meteostation read software started.\n")

path = "./data/"
StationName = "LKSO-M1"

try:
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)
except serial.SerialException:
    sys.stdout.write("Serial port could not be opened.\n")
    sys.exit(1)


msg = ["" for x in range(10)]

a = float('NaN')
b = float('NaN')
c = float('NaN')
d = float('NaN')

precipitation = float('NaN')
wind = float('NaN'), int()
wind_2min = float('NaN'), int()
wind_10min = float('NaN'), int()
dewpoint = float('NaN')
pressure_3h = float('NaN')
power = int()
alarm = int()
atmosphere_stability = int()
WAD_wind = float('NaN'), float('NaN'), int()
WAD_wind_2min = float('NaN'), float('NaN'), int()
WAD_wind_10min = float('NaN'), float('NaN'), int()

try:
    while True:
        byte = ser.read(1)
        if ord(byte) == 0x1E:
            msg = ser.read(9)

            if msg[0] == 'A':                    # Analog input 
                a = msg[1:7]
                if a == '    --':
                    a = float('NaN')
                else:
                    a = int(a)/10.0

            elif msg[0] == 'B':                    # Analog input 
                b = msg[1:7]
                if b == '    --':
                    b = float('NaN')
                else:
                    b = int(b)/10.0

            elif msg[0] == 'C':                    # Analog input 
                c = msg[1:7]
                if c == '    --':
                    c = float('NaN')
                else:
                    c = int(c)/10.0

            elif msg[0] == 'D':                    # Analog input 
                d = msg[1:7]
                if d == '    --':
                    d = float('NaN')
                else:
                    d = int(d)/10.0
                
            elif msg[0] == 'E':                    # precipitation input
                precipitation = int(msg[1:7])
                
            elif msg[0] == 'G':                    # wind speed and direction
                wind_direction =  int(msg[1:3]) * 10
                wind_speed =  int(msg[3:7])/10.0
                wind = (wind_speed), (wind_direction)
                
            elif msg[0] == 'H':                    # wind speed and direction (2 minutes sliding average)
                wind_direction =  int(msg[1:3]) * 10
                wind_speed =  int(msg[3:7])/10.0
                wind_2min = (wind_speed), (wind_direction)

            elif msg[0] == 'I':                    # wind speed and direction (10 minutes sliding average)
                wind_direction =  int(msg[1:3])* 10
                wind_speed =  int(msg[3:7])/10.0
                wind_10min = (wind_speed), (wind_direction )

            elif msg[0] == 'L':                    # Dewpoint temperature
                dewpoint = msg[1:7]
                if dewpoint == '    --':
                    dewpoint = float('NaN')
                else:
                    dewpoint = int(dewpoint)/10.0

            elif msg[0] == 'M':                    # 3hours pressure trend
                pressure_3h = int(msg[1:7])/10.0

            elif msg[0] == 'Q':                    # power status in % (0-100% is internal power capacity) if external power supply present value is greater than 100
                power = int(msg[1:7])

            elif msg[0] == 'R':                    # alarm or relay status
                alarm = int(msg[1:7])

            elif msg[0] == 'S':                    # atmospheric stability
                atmosphere_stability = int(msg[1:7])

            elif msg[0] == 'W':                    # WAD software special format
                wind_direction = 10*(16*(ord(msg[1]) & 0x0F) + (ord(msg[2]) & 0x0F))
                wind_speed =  256*(16*(ord(msg[3]) & 0x0F) + (ord(msg[4]) & 0x0F)) + 16*(ord(msg[5]) & 0x0F) + (ord(msg[6]) & 0x0F)
                wind_speed_ms = wind_speed / 37.38932004
                wind_speed_kt = wind_speed_ms * 1.943844492
                WAD_wind = (wind_speed_ms, wind_speed_kt, wind_direction )

            elif msg[0] == 'X':                    # WAD software special format 2 minutes average
                wind_direction = 10*(16*(ord(msg[1]) & 0x0F) + (ord(msg[2]) & 0x0F))
                wind_speed =  256*(16*(ord(msg[3]) & 0x0F) + (ord(msg[4]) & 0x0F)) + 16*(ord(msg[5]) & 0x0F) + (ord(msg[6]) & 0x0F)
                wind_speed_ms = wind_speed / 37.38932004
                wind_speed_kt = wind_speed_ms * 1.943844492
                WAD_wind_2min = (wind_speed_ms, wind_speed_kt, wind_direction )

            elif msg[0] == 'Y':                    # WAD software special format 10 minutes average
                wind_direction = 10*(16*(ord(msg[1]) & 0x0F) + (ord(msg[2]) & 0x0F))
                wind_speed =  256*(16*(ord(msg[3]) & 0x0F) + (ord(msg[4]) & 0x0F)) + 16*(ord(msg[5]) & 0x0F) + (ord(msg[6]) & 0x0F)
                wind_speed_ms = wind_speed / 37.38932004
                wind_speed_kt = wind_speed_ms * 1.943844492
                WAD_wind_10min = (wind_speed_ms, wind_speed_kt, wind_direction )

            now = datetime.datetime.now()
            filename = path + time.strftime("%Y%m%d%H", time.gmtime())+"0000_"+StationName+"_freq.csv"
            if not os.path.exists(filename):
                with open(filename, "a") as f:
                    f.write('#timestamp,Temperature,QFE,QNH,Wind_speed[m/s],Wind_direction \n')

	    temp = a
	    QFE = c
	    QNH = d

            with open(filename, "a") as f:
                f.write("%.1f,%3.1f,%4.1f,%4.1f,%3.1f,%3.1f\n" % (time.time(), temp, QFE, QNH, WAD_wind[0], WAD_wind[2] ))

            sys.stdout.write(" Temperature: %3.1f C\r\n" % (temp))
            sys.stdout.write(" Pressure: %3.1f hPa \r\n" % (b))
            sys.stdout.write(" QFE: %4.1f hPa\r\n" % (c))
            sys.stdout.write(" QNH: %4.1f hPa\r\n" % (d))
            sys.stdout.write(" Wind Speed: %3.1f kt Direction: %d \r\n" % (wind[0], wind[1]))
            sys.stdout.write(" Wind Speed: %3.1f kt Direction: %d  2 minutes average \r\n" % (wind_2min[0], wind_2min[1]))
            sys.stdout.write(" Wind Speed: %3.1f kt Direction: %d  10 minutes average\r\n" % (wind_10min[0], wind_10min[1]))
            sys.stdout.write(" Dewpoint: %3.1f \r\n" % (dewpoint))
            sys.stdout.write(" Pressure %4.1f hPa 3 hours trend.\r\n" % (pressure_3h))
            sys.stdout.write(" Power %d  \r\n" % (power))
            sys.stdout.write(" Alarm status %d \r\n" % (alarm))
            sys.stdout.write(" Atmospheric stability  %d \r\n" % (atmosphere_stability))
            sys.stdout.write(" WAD Wind: Speed: %3.1f m/s %3.1f kt Direction: %d  \r\n" % (WAD_wind[0], WAD_wind[1], WAD_wind[2]))
            sys.stdout.write(" WAD Wind: Speed: %3.1f m/s %3.1f kt Direction: %d 2 minutes average \r\n" % (WAD_wind_2min[0], WAD_wind_2min[1], WAD_wind_2min[2]))
            sys.stdout.write(" WAD Wind: Speed: %3.1f m/s %3.1f kt Direction: %d 10 minutes average \r\n" % (WAD_wind_10min[0], WAD_wind_10min[1], WAD_wind_10min[2]))
            sys.stdout.flush()

except KeyboardInterrupt:
    ser.close()
    f.close()
    sys.exit(0)

