import unittest
from src.ride_sharing import RideSharing


class TestRideSharing(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def _test(self, file_path: str, expected: str):
        ride_sharing = RideSharing()
        output = ride_sharing.process_file(file_path)
        self.assertEqual(output, expected)

    def test_input1(self):
        expected = """DRIVERS_MATCHED D1 D3
RIDE_STARTED RIDE-001
RIDE_STOPPED RIDE-001
BILL RIDE-001 D3 186.72"""
        self._test("./sample_input/input1.txt", expected)

    def test_input2(self):
        expected = """DRIVERS_MATCHED D2 D3 D1
DRIVERS_MATCHED D1 D2 D3
RIDE_STARTED RIDE-101
RIDE_STARTED RIDE-102
RIDE_STOPPED RIDE-101
RIDE_STOPPED RIDE-102
BILL RIDE-101 D2 234.64
BILL RIDE-102 D1 258.00"""
        self._test("./sample_input/input2.txt", expected)

    def test_input3(self):
        expected = """NO_DRIVERS_AVAILABLE
DRIVERS_MATCHED D13 D4 D2
RIDE_STARTED RIDE-001
RIDE_STOPPED RIDE-001
BILL RIDE-001 D13 268.36"""
        self._test("./sample_input/input3.txt", expected)

    def test_input4(self):
        expected = """NO_DRIVERS_AVAILABLE
DRIVERS_MATCHED D1
DRIVERS_MATCHED D2 D1
DRIVERS_MATCHED D14 D15 D16 D1
DRIVERS_MATCHED D15 D2 D1
RIDE_STARTED RIDE-001
DRIVERS_MATCHED D14 D16 D17 D1
RIDE_STOPPED RIDE-001
BILL RIDE-001 D15 327.20
RIDE_STARTED RIDE-002
RIDE_STOPPED RIDE-002
INVALID_RIDE
BILL RIDE-002 D17 440.26
INVALID_RIDE
BILL RIDE-002 D17 440.26"""
        self._test("./sample_input/input4.txt", expected)

    def test_input5(self):
        expected = """DRIVERS_MATCHED D1
DRIVERS_MATCHED D3 D1 D2
RIDE_STARTED RIDE-001
DRIVERS_MATCHED D6 D7 D5 D3 D4
DRIVERS_MATCHED D5 D6 D7 D3
RIDE_STOPPED RIDE-001
RIDE_STARTED RIDE-002
RIDE_STARTED RIDE-003
BILL RIDE-001 D1 96.67
RIDE_STOPPED RIDE-002
RIDE_STOPPED RIDE-003
BILL RIDE-003 D6 62.40
BILL RIDE-002 D7 79.80"""
        self._test("./sample_input/input5.txt", expected)


if __name__ == "__main__":
    unittest.main()
