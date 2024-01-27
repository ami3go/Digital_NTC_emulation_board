import machine
import time

# Initialize the USB virtual comm port
usb_vcp = machine.UART.init(0)

# Send data over USB virtual comm port
usb_vcp.write("Hello, RP2040!")

# Read data from USB virtual comm port
data = usb_vcp.read(10)  # Read 10 bytes

# Print the received data
print("Received data:", data)

# Close the USB virtual comm port
usb_vcp.close()