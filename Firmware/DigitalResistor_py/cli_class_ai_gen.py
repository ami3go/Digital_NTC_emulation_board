import machine
import time

class <link>UART_CLI</link>:
    def __init__(self, uart_num, baudrate):
        self.uart = machine.UART(uart_num, baudrate=baudrate)

    def process_command(self, cmd_with_params):
        cmd, *params = cmd_with_params.split()
        if cmd == 'led':
            if params[0] == 'on':
                # Turn on the LED based on the parameter
                # Example: machine.Pin(2, machine.Pin.OUT).on()
                self.uart.write('LED turned on\n')  # Respond to the command
            elif params[0] == 'off':
                # Turn off the LED based on the parameter
                # Example: machine.Pin(2, machine.Pin.OUT).off()
                self.uart.write('LED turned off\n')  # Respond to the command
            else:
                self.uart.write('Unknown parameter for LED command\n')  # Respond if the parameter is not recognized
        elif cmd == 'servo':
            # Control servo motor based on the parameter
            # Example: servo_pin = machine.PWM(machine.Pin(2)); servo_pin.duty(int(params[0]))
            self.uart.write('Servo action performed\n')  # Respond to the command
        else:
            self.uart.write('Unknown command\n')  # Respond if the command is not recognized

# Usage
uart_cli = <link>UART_CLI</link>(uart_num=0, baudrate=115200)
while True:
    if uart_cli.uart.any():  # Check if there's any data available to read
        cmd_with_params = uart_cli.uart.readline().decode().strip()  # Read the command with parameters from UART and decode it
        uart_cli.process_command(cmd_with_params)  # Process the command
