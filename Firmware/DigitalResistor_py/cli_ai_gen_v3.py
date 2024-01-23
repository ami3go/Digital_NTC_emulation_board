import machine

class UART_CLI:
    def __init__(self, uart_num, baudrate):
        self.uart = machine.UART(uart_num, baudrate=baudrate)
        self.commands = {}  # Dictionary to store commands and their corresponding actions

    def add_command(self, command, action, max_params=3):
        self.commands[command] = (action, max_params)  # Store the action and maximum parameters for the command

    def process_command(self, cmd_with_params):
        cmd, *params = cmd_with_params.split()
        if cmd in self.commands:
            action, max_params = self.commands[cmd]  # Retrieve the action and maximum parameters for the command
            if len(params) <= max_params:
                action(*params)  # Execute the action with the provided parameters
            else:
                self.uart.write('Too many parameters for command {}\n'.format(cmd))  # Respond if too many parameters are provided
        else:
            self.uart.write('Unknown command\n')  # Respond if the command is not recognized

# Usage
def set_servo_position(param1, param2, param3):
    # Custom action to set the servo motor position based on the parameters
    pass  # Replace with actual code to control the servo motor

def custom_action_with_two_params(param1, param2):
    # Custom action with two parameters
    pass  # Replace with actual code for the custom action

uart_cli = UART_CLI(uart_num=0, baudrate=115200)
uart_cli.add_command('set_servo', set_servo_position, max_params=3)  # Add a custom command "set_servo" with a maximum of 3 parameters
uart_cli.add_command('custom_action', custom_action_with_two_params, max_params=2)  # Add a custom command "custom_action" with a maximum of 2 parameters

while True:
    if uart_cli.uart.any():  # Check if there's any data available to read
        cmd_with_params = uart_cli.uart.readline().decode().strip()  # Read the command with parameters from UART and decode it
        uart_cli.process_command(cmd_with_params)  # Process the command
