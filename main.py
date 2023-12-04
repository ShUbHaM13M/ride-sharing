from ast import Dict
from sys import argv
import sys


commands = {
    "ADD_DRIVER": ["DRIVER_ID", "X_COORDINATE", "Y_COORDINATE"],
    "ADD_RIDER": ["RIDER_ID", "X_COORDINATE", "Y_COORDINATE"],
    "MATCH": ["RIDER_ID"],
    "START_RIDE": ["RIDE_ID", "N", "RIDER_ID"],
    "STOP_RIDE": [
        "RIDE_ID",
        "DESTINATION_X_COORDINATE",
        "DESTINATION_Y_COORDINATE",
        "TIME_TAKEN_IN_MIN",
    ],
    "BILL": ["RIDE_ID"],
}

drivers = {}
riders = {}


def add_driver(info: Dict[str, str | int]):
    drivers[info["DRIVER_ID"]] = {
        "x": int(info["X_COORDINATE"]),
        "y": int(info["Y_COORDINATE"]),
    }
    print(f"Added Driver: {info['DRIVER_ID']}")


def process_command(command: str):
    command = command.split(" ")
    command, args = command[0], command[1:]
    _command = commands.get(command)
    if _command == None:
        raise Exception(f"{command}: Command not found")
    else:
        if len(_command) != len(args):
            raise Exception(f"Not enough args passed for command: {command}")

        arg_map = {}
        for key, value in zip(_command, args):
            arg_map[key] = value

        if command == "ADD_DRIVER":
            add_driver(arg_map)
        elif command == "ADD_RIDER":
            riders[arg_map["RIDER_ID"]] = {
                "x": int(arg_map["X_COORDINATE"]),
                "y": int(arg_map["Y_COORDINATE"]),
            }
            print(f"Added Rider: {arg_map['RIDER_ID']}")
        else:
            print("Error: Command Not Yet Implemented", file=sys.stderr)


def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]

    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line[0] != "#":
                process_command(line.rstrip())


if __name__ == "__main__":
    main()
