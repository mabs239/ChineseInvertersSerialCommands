
This project started at interfacing the Inverex Veryon II 1200W-12V solar hybrid inverter. This inverter is a label version of many Chinese knock offs such as Axper, Solarmax, mpp solar etc. These inverters come with a serial port, built into RJ45, and can be connected to PC, wither using serial port or using USB to Serial converter.

# modbus.py
The "modbus3.py" file queries a custom command from the inverter and displays its result in text format.

Example: 
C:\Users\GhulamNabi>python modbus.py QPIGS
Sending command:
b'QPIGS\xb7\xa9\r'
Printing reply from inverter:
(228.8 49.6 228.8 49.6 0000 0000 000 357 12.20 000 095 0039 00.0 000.0 00.00 00000 00010100 00 00 00000 010,

28 32 32 38 2E 38 20 34 39 2E 36 20 32 32 38 2E 38 20 34 39 2E 36 20 30 30 30 30 20 30 30 30 30 20 30 30 30 20 33 35 37 20 31 32 2E 32 30 20 30 30 30 20 30 39 35 20 30 30 33 39 20 30 30 2E 30 20 30 30 30 2E 30 20 30 30 2E 30 30 20 30 30 30 30 30 20 30 30 30 31 30 31 30 30 20 30 30 20 30 30 20 30 30 30 30 30 20 30 31 30 2C 0D


The name is modbus because project started as implementation of modbus. Later it was found that text commands are accepted. QPIGS is a inverter Query for Parameter Information for General Settings. 

# boot.py
This is a bootfile for ESP32 running micropython. It queries QPIGS from inverter and sends read data to ThingSpeak channel.
