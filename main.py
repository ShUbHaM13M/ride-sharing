import math
from typing import Dict
from sys import argv
import sys

MAX_RANGE = 5

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


def add_driver(info: Dict[str, str]):
    driver_id = info["DRIVER_ID"]
    try:
        drivers[driver_id] = [
            int(info["X_COORDINATE"]),
            int(info["Y_COORDINATE"]),
        ]
        print(f"Added Driver: {driver_id}")
    except ValueError:
        print(f"Error: Coordinate values of Rider {driver_id} is not a number")
        sys.exit(1)


def add_rider(info: Dict[str, str]):
    rider_id = info["RIDER_ID"]
    try:
        riders[rider_id] = [
            int(info["X_COORDINATE"]),
            int(info["Y_COORDINATE"]),
        ]
        print(f"Added Rider: {rider_id}")
    except ValueError:
        print(f"Error: Coordinate values of Rider {rider_id} is not a number")
        sys.exit(1)


def match_rider(info: Dict[str, str]):
    rider_id = info["RIDER_ID"]
    rider_pos = riders[rider_id]
    drivers_in_range = []

    for driver_id, driver_pos in drivers.items():
        distance = math.floor(math.dist(rider_pos, driver_pos))
        if distance <= MAX_RANGE:
            driver = {
                "id": driver_id,
                "pos": drivers[driver_id],
                "distance": distance,
            }
            drivers_in_range.append(driver)

    if len(drivers_in_range) == 0:
        print("NO_DRIVERS_AVAILABLE")
        return

    drivers_in_range.sort(key=lambda x: x["distance"])

    temp = drivers_in_range[0]["distance"]
    equidistant = all(val["distance"] == temp for val in drivers_in_range)
    if equidistant:
        # TODO: Sort using lexicographical order
        pass

    print("DRIVERS_MATCHED", end=" ")
    for driver in drivers_in_range:
        print(driver["id"], end=" ")
    print("")


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
            add_rider(arg_map)
        elif command == "MATCH":
            match_rider(arg_map)
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
