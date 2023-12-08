import math
from typing import Dict
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


MAX_RANGE = 5.0
BASE_FARE_AMOUNT = 50.0
DISTANCE_AMOUNT = 6.5
TIME_AMOUNT = 2.0
SERVICE_TAX = 0.2


class RideSharing:
    def __init__(self) -> None:
        self.drivers = {}
        self.riders = {}
        self.matched_rides = {}
        self.rides = {}

    def process_file(self, file_path: str):
        output = []
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == "#":
                    continue
                data = self.process_command(line.rstrip())
                if data:
                    output.append(data)

        return "\n".join(output)

    def add_driver(self, arg: Dict[str, str]):
        driver_id = arg["DRIVER_ID"]
        try:
            self.drivers[driver_id] = {
                "id": driver_id,
                "pos": [int(arg["X_COORDINATE"]), int(arg["Y_COORDINATE"])],
                "occupied": False,
            }
        except ValueError:
            print(f"Error: Coordinate values of Rider {driver_id} is not a number")
            sys.exit(1)

    def add_rider(self, arg: Dict[str, str]):
        rider_id = arg["RIDER_ID"]
        try:
            self.riders[rider_id] = {
                "id": rider_id,
                "pos": [
                    int(arg["X_COORDINATE"]),
                    int(arg["Y_COORDINATE"]),
                ],
            }
        except ValueError:
            print(f"Error: Coordinate values of Rider {rider_id} is not a number")
            sys.exit(1)

    def match_rider(self, arg: Dict[str, str]):
        rider_id = arg["RIDER_ID"]
        rider_pos = self.riders[rider_id]["pos"]
        drivers_in_range = []
        for driver_id, driver in self.drivers.items():
            distance = math.dist(rider_pos, driver["pos"])
            if distance <= MAX_RANGE and not driver["occupied"]:
                driver = {
                    "id": driver_id,
                    "pos": self.drivers[driver_id],
                    "distance": distance,
                }
                drivers_in_range.append(driver)

        if len(drivers_in_range) == 0:
            return "NO_DRIVERS_AVAILABLE"

        drivers_in_range.sort(key=lambda x: (x["distance"], x["id"]))
        self.matched_rides[rider_id] = drivers_in_range

        output = "DRIVERS_MATCHED"
        for driver in drivers_in_range:
            output += f" {driver['id']}"
        return output

    def start_ride(self, arg: Dict[str, str]):
        ride_id, driver_index, rider_id = arg.values()

        try:
            driver_index = int(driver_index)
        except ValueError:
            raise Exception(f"Driver index: {driver_index} is not a number")

        if 1 > driver_index or self.matched_rides.get(ride_id) != None:
            return "INVALID_RIDE"

        if selected_ride := self.matched_rides.get(rider_id):
            if driver_index > len(selected_ride) or self.rides.get(ride_id):
                return "INVALID_RIDE"

            driver_id = selected_ride[driver_index - 1]["id"]
            self.drivers[driver_id]["occupied"] = True

            self.rides[ride_id] = {
                "rider_id": rider_id,
                "driver": self.drivers[driver_id],
                "started": True,
            }
            return f"RIDE_STARTED {ride_id}"
        else:
            return "INVALID_RIDE"

    def stop_ride(self, arg: Dict[str, str]):
        ride_id, destination_x, destination_y, time_taken = arg.values()

        if (selected_ride := self.rides.get(ride_id)) != None:
            if not selected_ride["started"]:
                return "INVALID_RIDE"
            selected_ride["started"] = False

            try:
                destination = [int(destination_x), int(destination_y)]
                selected_ride.update(
                    {
                        "destination": destination,
                        "time_taken": int(time_taken),
                    }
                )
                driver_id = selected_ride["driver"]["id"]
                self.drivers[driver_id] = destination
                return f"RIDE_STOPPED {ride_id}"
            except ValueError:
                print(
                    "Error: Values of destination or time taken is not number",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            return "INVALID_RIDE"

    def bill(self, arg: Dict[str, str]):
        (ride_id,) = arg.values()
        total_amount: float = BASE_FARE_AMOUNT
        if selected_ride := self.rides.get(ride_id):
            if selected_ride["started"]:
                return "RIDE_NOT_COMPLETED"

            driver_id = selected_ride["driver"]["id"]

            start = self.riders[selected_ride["rider_id"]]["pos"]
            destination = selected_ride["destination"]
            distance = math.dist(start, destination)
            distance = round(distance, 2)

            total_amount += selected_ride["time_taken"] * TIME_AMOUNT
            total_amount += distance * DISTANCE_AMOUNT
            total_amount += round(total_amount * SERVICE_TAX, 2)

            return f"BILL {ride_id} {driver_id} {total_amount:.2f}"
        else:
            return "INVALID_RIDE"

    def process_command(self, command):
        command = command.split(" ")
        command, args = command[0], command[1:]
        _command = commands.get(command)
        if _command == None:
            raise Exception(f"{command}: Command not found")
        if len(_command) != len(args):
            raise Exception(f"Not enough args passed for command: {command}")

        arg_map = {}
        for key, value in zip(_command, args):
            arg_map[key] = value

        if command == "ADD_DRIVER":
            self.add_driver(arg_map)
        elif command == "ADD_RIDER":
            self.add_rider(arg_map)
        elif command == "MATCH":
            return self.match_rider(arg_map)
        elif command == "START_RIDE":
            return self.start_ride(arg_map)
        elif command == "STOP_RIDE":
            return self.stop_ride(arg_map)
        elif command == "BILL":
            return self.bill(arg_map)
        else:
            print("Error: Command Not Yet Implemented", file=sys.stderr)
