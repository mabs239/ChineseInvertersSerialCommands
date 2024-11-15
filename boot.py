########################################################
# Allah to be praised and countless blessings on 
# His Last Prophet Hazrat Muhammad (peace be upon him)
########################################################

import urequests
from machine import UART, Pin, RTC
import time
import network
import ntptime


# Wi-Fi credentials
SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'
rtc = RTC()
# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    print("Wi-Fi connected:", wlan.ifconfig())

# Set RTC using NTP server
def set_time():
    try:
        # Set the NTP server (for Pakistan)
        ntptime.host = 'pk.pool.ntp.org'
        
        # Get the time from the NTP server and set the RTC
        ntptime.settime()
        print("RTC successfully set to:", time.localtime())
    except Exception as e:
        print("Failed to set time:", e)

nw = network.WLAN(network.STA_IF); 
nw.active(True)
print(nw.scan())
nw.connect('ssid','password')

while not nw.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
print("Connected to Wi-Fi:", nw.ifconfig())


u2 = UART(2, baudrate=2400, tx=17, rx=16)
#while True:
qpigs = b'QPIGS\xb7\xa9\r'
qpiri = b'QPIRI\xf8T\r'
qdi = b'QDIq\x1b\r'

u2.write(qpigs)
time.sleep(1)
in1= u2.read()
print(in1)
print(b'(V_in  f_in V_out f_o  P_va P_w  Ld% Vbus V_bt Ich Bt% Tinv I_pv V_pv  Vscc  Ibt_d          FN EV P_pv     ')
#     b'(232.5 49.9 232.5 49.9 0279 0221 023 405 13.80 007 095 0048 01.4 083.2 00.00 00000 01010110 00 00 00122 010\xb2\x00\r')
#     b'(01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789 \r')
P_w = float(in1[27:32])
Vbus = float(in1[36:40])
Vbat = float(in1[40:46])
Ich = float(in1[46:50])
Tinv = float(in1[54:59])
I_pv = float(in1[59:64])
V_pv = float(in1[64:70])
P_pv = float(in1[97:103])

print(P_w, Vbus, Vbat, Ich, Tinv, I_pv, V_pv, P_pv)






# Parameters
MAX_RETRIES = 10
THINGSPEAK_APIKEY = 'apikey'  # Replace with your actual API key
url = "http://api.thingspeak.com/update"

print("Welcome to the ThingSpeak ESP32 demonstration!")
print("Press CTRL+C to stop.")

# Helper function to create URL-encoded data manually
def urlencode(params):
    return '&'.join('{}={}'.format(key, value) for key, value in params.items())

# Main loop
while True:
    # Generate reading
    u2.write(qpigs)
    time.sleep(1)
    in1= u2.read()
    print(in1)
    print(b'(V_in  f_in V_out f_o  P_va P_w  Ld% Vbus V_bt Ich Bt% Tinv I_pv V_pv  Vscc  Ibt_d          FN EV P_pv     ')
    #     b'(232.5 49.9 232.5 49.9 0279 0221 023 405 13.80 007 095 0048 01.4 083.2 00.00 00000 01010110 00 00 00122 010\xb2\x00\r')
    #     b'(01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789 \r')
    P_w = float(in1[27:32])
    P_pv = float(in1[97:103])
    Vbat = float(in1[40:46])
    Ich = float(in1[46:50])
    Ibt_d = float(in1[76:82])
    Tinv = float(in1[54:59])
    I_pv = float(in1[59:64])
    V_pv = float(in1[64:70])
    Vbus = float(in1[36:40])

    set_time()
    print("Current time:", rtc.datetime())
# Adjust NTP time to local PST (UTC+5)
    local_time = list(rtc.datetime())
    local_time[4] += 5  # Add 5 hours to UTC time
    if local_time[4] >= 24:
        local_time[4] -= 24
        local_time[2] += 1  # Adjust the day (simple example without month-end check)
    print("Local Time:", tuple(local_time))
    
    
    # Prepare data to send, and convert it to bytes
    #param_dict = {'field1': rand_int, 'api_key': THINGSPEAK_APIKEY}
    param_dict = {
        'field1': P_w,
        'field2': Vbat,
        'field3': P_pv,
        'field4': (Ich-Ibt_d),
        'field5': Tinv,
        'field6': I_pv,
        'field7': V_pv,
        'field8': Vbus,
        'api_key': THINGSPEAK_APIKEY
    }
    params = urlencode(param_dict)
    data = params.encode('utf-8')  # Convert the URL-encoded string to bytes

    retry = 0
    
    # Retry loop
    while retry <= MAX_RETRIES:
        try:
            response = urequests.post(url, data=data)
            if response.status_code != 200:
                print("Response: {} {}".format(response.status_code, response.reason))
                print("Data returned:", response.text)  # Diagnostic data
            else:
                print("Channel update successful.")
            response.close()
            break  # Exit retry loop on success
        except Exception as err:
            print("WARNING: ThingSpeak connection failed:", err)
            if retry < MAX_RETRIES:
                print("Retrying in 5 seconds. [{}]".format(retry + 1))
                time.sleep(5)
                retry += 1
            else:
                print("WARNING: Cannot send data. Exceeded retries.")
                break
    
    # Wait before the next update
    time.sleep(30)

