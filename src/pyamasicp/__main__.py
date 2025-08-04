import logging
import sys

from .client import Client
from .commands import Commands

if __name__ == '__main__':
    import argparse

    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)

    # Set levels for handlers
    stdout_handler.setLevel(logging.DEBUG)
    stderr_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    logging.basicConfig(handlers=[stdout_handler, stderr_handler])

    parser = argparse.ArgumentParser(description='Example script.')
    parser.add_argument('command', type=str, help='Command to execute')
    parser.add_argument('arguments', nargs='*', type=str, help='Arguments to the command')
    parser.add_argument('-t', '--target', required=True, help='Hostname or IP of the target RS232 device.')
    parser.add_argument('-p', '--port', default=5000, help='Port on which the target RS232 device listens.')

    args = parser.parse_args()

    commands = Commands(Client(args.target, port=args.port))
    if args.command == 'volume':
        if args.arguments:
            commands.set_volume(int(args.arguments[0]),
                                int(args.arguments[0] if len(args.arguments) < 2 else int(args.arguments[1])))
        print("Volume is: %s\n" % commands.get_volume())
