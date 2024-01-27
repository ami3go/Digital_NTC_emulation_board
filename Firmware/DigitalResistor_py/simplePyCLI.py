
class simplePyCLI:
    def __init__(self, cli_symbol):
        self.commands = {}  # Dictionary to store commands and their corresponding actions
        self.cursor = cli_symbol
    def add_command(self, command, action, max_params=3, description=""):
        self.commands[command] = (action, max_params, description)  # Store the action and maximum parameters for the command
        # print(self.commands)
    def process_command(self, cmd_with_params):
        cmd, *params = cmd_with_params.split()
        in_var = cmd_with_params.split()
        if cmd in self.commands:
            action, max_params, help = self.commands[cmd]  # Retrieve the action and maximum parameters for the command

            #print(in_var, "given:", len(params), "max:", max_params)

            if len(params) > max_params:
                print(f'ERROR, {self.cursor}{in_var} -> Too many parameters. Given: {len(params)}, Requires: {max_params}')
            elif len(params) == max_params:
                print(f"OK, {self.cursor}{in_var}")
                action(*params)  # Execute the action with the provided parameters
            elif len(params) < max_params:
                print(f'ERROR, {self.cursor}{in_var} -> Missing parameters. Given: {len(params)}, Requires: {max_params}')  # Respond if the command is not recognized
            else:
                print(f'ERROR, {self.cursor}{in_var} -> Unknown error ')  # Respond if
        elif cmd == "help":
            self._print_help()
        else:
            print(f'ERROR, {self.cursor}{in_var} Unknown command. Use "help" for supported commands ')  # Respond if the command is not recognized
    def _print_help(self, cmd=""):
        cmd_keys = list(self.commands.keys())
        n=30
        print("#"*n, "HELP", "#"*n)
        for cmd in cmd_keys:
            action, params, help = self.commands[cmd]
            print(f"{self.cursor} {cmd} params:{params}, Desc: {help}")
        print("#" * n, "HELP", "#" * n)

