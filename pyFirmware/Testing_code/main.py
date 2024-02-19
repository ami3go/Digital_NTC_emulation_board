import machine
import os
import time
import sdcard
import utime
# Remapped SPI pin numbers
MOSI_PIN = 3
MISO_PIN = 4
SCK_PIN = 2
CS_PIN = 5

# Set up SPI communication with the SD card
spi = machine.SPI(0, baudrate=10000000, polarity=0, phase=0, sck=machine.Pin(SCK_PIN), mosi=machine.Pin(MOSI_PIN), miso=machine.Pin(MISO_PIN))
cs = machine.Pin(CS_PIN, machine.Pin.OUT)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, '/sd')

# Create a file on the SD card
filename = '/sd/test.txt'
# Write data to the file
with open(filename, 'w') as f:
    data = bytearray(1024)  # Data buffer of 1024 bytes
    start_time = utime.ticks_ms()
    f.write(data)
    write_time = utime.ticks_diff(utime.ticks_ms(), start_time)
    print("Write time:", write_time, "ms")

# Read data from the file
with open(filename, 'rb') as f:
    start_time = utime.ticks_ms()
    f.readinto(data)
    read_time = utime.ticks_diff(utime.ticks_ms(), start_time)
    print("Read time:", read_time, "ms")

# Unmount the SD card
os.umount('/sd')