import math
from typing import Dict
from sys import argv
import sys

MAX_RANGE = 5
BASE_FARE_AMOUNT = 50
DISTANCE_AMOUNT = 6.5
TIME_AMOUNT = 2
SERVICE_TAX = 0.2

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
matched_rides = {}
rides = {}


def add_driver(info: Dict[str, str]):
    driver_id = info["DRIVER_ID"]
    try:
        drivers[driver_id] = [
            int(info["X_COORDINATE"]),
            int(info["Y_COORDINATE"]),
        ]
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

    drivers_in_range.sort(key=lambda x: (x["distance"], x["id"]))
    matched_rides[rider_id] = drivers_in_range

    print("DRIVERS_MATCHED", end=" ")
    for driver in drivers_in_range:
        print(driver["id"], end=" ")
    print("")


def start_ride(arg: Dict[str, str]):
    ride_id, driver_index, rider_id = arg.values()

    try:
        driver_index = int(driver_index)
    except ValueError:
        raise Exception(f"Driver index: {driver_index} is not a number")

    if 1 > driver_index or matched_rides.get(ride_id) != None:
        print("INVALID_RIDE")
        return

    if selected_ride := matched_rides.get(rider_id):
        if driver_index > len(selected_ride) or rides.get(ride_id):
            print("INVALID_RIDE")
            return
        rides[ride_id] = {
            "rider_id": rider_id,
            "driver": selected_ride[driver_index - 1],
            "started": True,
        }
        print(f"RIDE_STARTED {ride_id}")
    else:
        print("INVALID_RIDE")
        return


def stop_ride(arg: Dict[str, str]):
    ride_id, destination_x, destination_y, time_taken = arg.values()

    if (selected_ride := rides.get(ride_id)) != None:
        if not selected_ride["started"]:
            print("INVALID_RIDE")
            return
        selected_ride["started"] = False

        try:
            selected_ride.update(
                {
                    "destination": [int(destination_x), int(destination_y)],
                    "time_taken": int(time_taken),
                }
            )
            print(f"RIDE_STOPPED {ride_id}")
        except ValueError:
            print("Error: Values of destination or time taken is not number")
            sys.exit(1)
    else:
        print("INVALID_RIDE")
        return


def bill(arg: Dict[str, str]):
    (ride_id,) = arg.values()
    total_amount: float = BASE_FARE_AMOUNT

    if selected_ride := rides.get(ride_id):
        if selected_ride["started"]:
            print("RIDE_NOT_COMPLETED")
            return

        driver_id = selected_ride["driver"]["id"]

        start = riders[selected_ride["rider_id"]]
        destination = selected_ride["destination"]
        distance = math.dist(start, destination)
        distance = round(distance, 2)

        total_amount += selected_ride["time_taken"] * TIME_AMOUNT
        total_amount += distance * DISTANCE_AMOUNT
        total_amount += total_amount * SERVICE_TAX

        print(f"BILL {ride_id} {driver_id} {total_amount:.2f}")
    else:
        print("INVALID_RIDE")
        return


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
        elif command == "START_RIDE":
            start_ride(arg_map)
        elif command == "STOP_RIDE":
            stop_ride(arg_map)
        elif command == "BILL":
            bill(arg_map)
        else:
            print("Error: Command Not Yet Implemented", file=sys.stderr)


def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]

    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == "#":
                continue
            process_command(line.rstrip())


if __name__ == "__main__":
    main()
