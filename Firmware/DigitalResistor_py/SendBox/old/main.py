import sys

def main():
    print("Welcome to the Simple CLI!")
    print("Type 'exit' to quit.")

    while True:
        # Print cursor
        sys.stdout.write("> ")
        sys.stdout.flush()

        # Read input from stdin
        user_input = sys.stdin.readline().strip()

        # Process the input
        if user_input == 'exit':
            print("Exiting...")
            break
        else:
            print("You entered:", user_input)

if __name__ == "__main__":
    main()
