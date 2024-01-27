from machine import Pin
import neopixel

class LEDController:
    def __init__(self, pin_number, num_leds):
        self.led_pin = Pin(pin_number, Pin.OUT)
        self.led = neopixel.NeoPixel(self.led_pin, num_leds)

    def set_color(self, index, color):
        self.led[index] = color
        self.led.write()

    def fill_color(self, color):
        for i in range(len(self.led)):
            self.led[i] = color
        self.led.write()

    def clear(self):
        self.fill_color((0, 0, 0))