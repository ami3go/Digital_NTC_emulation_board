import machine

class UART_CLI:
    def __init__(self, uart_num, baudrate):
        self.uart = machine.UART(uart_num, baudrate=baudrate)
        self.commands = {}  # Dictionary to store commands and their corresponding actions

    def add_command(self, command, action):
        self.commands[command] = action

    def process_command(self, cmd_with_params):
        cmd, *params = cmd_with_params.split()
        if cmd in self.commands:
            action = self.commands[cmd]  # Retrieve the action for the command
            action(*params)  # Execute the action with the provided parameters
        else:
            self.uart.write('Unknown command\n')  # Respond if the command is not recognized

# Usage
def turn_on_led(param):
    # Custom action to turn on the LED based on the parameter
    pass  # Replace with actual code to turn on the LED

def turn_off_led(param):
    # Custom action to turn off the LED based on the parameter
    pass  # Replace with actual code to turn off the LED

uart_cli = UART_CLI(uart_num=0, baudrate=115200)
uart_cli.add_command('led_on', turn_on_led)  # Add a custom command "led_on" with the corresponding action
uart_cli.add_command('led_off', turn_off_led)  # Add a custom command "led_off" with the corresponding action

while True:
    if uart_cli.uart.any():  # Check if there's any data available to read
        cmd_with_params = uart_cli.uart.readline().decode().strip()  # Read the command with parameters from UART and decode it
        uart_cli.process_command(cmd_with_params)  # Process the command
