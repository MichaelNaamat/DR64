#!/usr/bin/env python3

import sys
from dataclasses import dataclass

import script_defs as defs

@dataclass(frozen=False)

# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# PMIC Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class PMICTester:
    REG_DEVICEID = "0x2B"

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Constructor Method to initialize the PMICTester 
    # class with a list of chip definitions and a remote 
    # client for communication
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, chips: list[defs.CChipDef], rem_client: defs.CBaseClient):
        self.chips = chips
        self.rem_client = rem_client

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Print Header Method to display a header for the chip being tested
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _print_header(self, chip: defs.CChipDef) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing PMIC {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Check Device Method to read the device ID from the chip
    # and print the result
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)
        dev_id = self.rem_client.i2c_get(chip.bus, chip.dev, self.REG_DEVICEID, "w")
        print(f"{defs.C_BLUE_B}  >>> DEBUG: Device ID={dev_id}{defs.C_NONE}")

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Run Method to iterate through the list of chips and 
    # check each device
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=<< Function >>-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main() -> int:
    chips = [
        defs.CChipDef(name="U54", bus="0x04", dev="0x20"),
        defs.CChipDef(name="U54", bus="0x04", dev="0x21"),
    ]
    
    Appl = defs.CApplication(sys.argv)
    rem_client = Appl.create_remote_client()
      
    rem_client.connect()
    PMICTester(chips, rem_client).run()
    rem_client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
