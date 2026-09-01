#!/usr/bin/env python3

import subprocess
import sys
from dataclasses import dataclass
from typing import List

import script_defs as defs

@dataclass(frozen=False)
# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# Power Supply Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class PowerSupplyTester:
    REG_VSET = "0x00"
    REG_CONTROL1 = "0x01"
    REG_CONTROL2 = "0x02"
    REG_CONTROL3 = "0x03"
    REG_STATUS = "0x04"

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Constructor Method to initialize the PowerSupplyTester 
    # class with a list of chip definitions and a remote
    # client for communication
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, chips: List[defs.CChipDef], ssh_client: defs.CBaseClient):
        self.chips = chips
        self.ssh_client = ssh_client

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Print Header Method to display a header for the chip 
    # being tested
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _print_header(self, chip: defs.CChipDef) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing Power Supply {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Check Device Method to verify the functionality of the 
    # power supply
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)

        vset = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_VSET, "w")
        control1 = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_CONTROL1)
        control2 = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_CONTROL2)
        control3 = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_CONTROL3)
        status   = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_STATUS)

        print(
            f"{defs.C_BLUE_B}  >>> DEBUG: VSET={vset}, Control1={control1}, "
            f"Control2={control2}, Control3={control3}, Status={status}{defs.C_NONE}"
        )

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Run Method to execute the power supply tests for all chips
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-  
def main() -> int:
    chips = [
        defs.CChipDef(name="U33"   , bus="0x01", dev="0x33"),
        defs.CChipDef(name="A_U26" , bus="0x01", dev="0x40"),
        defs.CChipDef(name="A_U18" , bus="0x01", dev="0x43"),
        defs.CChipDef(name="A_U100", bus="0x01", dev="0x46"),
        defs.CChipDef(name="U32"   , bus="0x02", dev="0x30"),
        defs.CChipDef(name="B_U26" , bus="0x02", dev="0x40"),
        defs.CChipDef(name="U34"   , bus="0x02", dev="0x43"),
        defs.CChipDef(name="B_U100", bus="0x02", dev="0x46"),
    ]
    Appl = defs.CApplication(sys.argv)
    rem_client = Appl.create_remote_client()
    rem_client.connect()
    PowerSupplyTester(chips, rem_client).run()
    rem_client.close()
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
