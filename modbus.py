#########################################################
# Allah to be praised and countless blessings on        #
# His Last Prophet Hazrat Muhammad (peace be upon him)  #
#########################################################
import serial
import time
import binascii
import sys

def calculate_crc16_xmodem(instr): # Calculate and append CRC for inverter command
    # Convert the input string to bytes
    data_bytes = instr.encode('utf-8')
    # Calculate the CRC-16/XMODEM checksum
    crc = binascii.crc_hqx(data_bytes, 0x0000)
    # Convert the CRC to a 2-byte big-endian byte sequence
    crc_bytes = crc.to_bytes(2, byteorder='big')
    # Append the CRC bytes to the original data
    outstr = data_bytes + crc_bytes + b'\x0D'  # Adding <cr> at end 0x0d
    return outstr

def string_to_hex_ascii(instr): # To display inverter response in hex
    hex_output = " ".join(f"{ord(c):02X}" for c in instr)
    return hex_output

def send_command(CMD): # Send commad to inverter on serial port
    ser2.write(CMD)
    time.sleep(2)  # 2 seconds delay
    if ser2.in_waiting > 0:
        response = ser2.read(ser2.in_waiting).decode(errors='ignore')
    else:
        print("No response received.")
    return response

# Initialize serial communication port
#serial_port = '/dev/ttyS0'  # Replace with your port name
serial_port = 'COM26'  # Replace with your port name
baud_rate_serial2 = 2400
timeout_duration = 0.02  # 20 milliseconds
ser2 = serial.Serial(serial_port, baud_rate_serial2, timeout=timeout_duration)

# Main function
def main():
    # Get the command from command-line arguments, default to "QMOD" if not provided
    CMD1 = sys.argv[1] if len(sys.argv) > 1 else "QMOD"
    
    # Open the file "COMMANDS.TXT" in append mode
    with open("COMMANDS.TXT", "a") as file:
        if ser2.is_open:
            CMD1b = calculate_crc16_xmodem(CMD1)  # Byte streamed
            file.write("Sending command:\n")
            file.write(f"{CMD1b}\n")
            print("Sending command:\n")
            print(f"{CMD1b}\n")
            
            response = send_command(CMD1b)
            file.write("Printing reply from inverter:\n")
            file.write(f"{response}\n")
            print("Printing reply from inverter:\n")
            print(f"{response}\n")
            
            file.write(f"{string_to_hex_ascii(response)}\n")
            file.write("\n")  # Add a newline for readability between entries
            print(f"{string_to_hex_ascii(response)}\n")
            print("\n")  # Add a newline for readability between entries
            
            print("Outputs have been appended to COMMANDS.TXT.")
        else:
            file.write("Failed to open serial ports.\n")
            print("Failed to open serial ports.")

if __name__ == "__main__":
    main()

