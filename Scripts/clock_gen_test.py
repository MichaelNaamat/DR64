#!/usr/bin/env python3

import subprocess
import sys
from dataclasses import dataclass
from typing import List, Optional

import script_defs as defs

@dataclass(frozen=True)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Clock-Gen Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class ClockGenTester:
    REG_DEVICE_PN_BASE = "0x0D"
    REG_DEVICE_REV = "0x0E"

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, chips: List[defs.CChipDef], i2c_client: defs.I2CClient): 
        self.chips = chips
        self.i2c_client = i2c_client

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _print_header(self, chip: defs.CChipDef) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing Clock-Gen {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")
        
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)
        dev_pn = self.i2c_client.get(chip.bus, chip.dev, self.REG_DEVICE_PN_BASE)
        dev_rev = self.i2c_client.get(chip.bus, chip.dev, self.REG_DEVICE_REV)
        print(f"{defs.C_BLUE_B}  >>> DEBUG: Device PN={dev_pn}, Device REV={dev_rev}{defs.C_NONE}")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main() -> int:
    chips = [
        defs.CChipDef(name="U87", bus="0x01", dev="0x6A"),
        defs.CChipDef(name="U88", bus="0x01", dev="0x6B"),
    ]
    defs.configure_modes(sys.argv)
    i2c_client = defs.I2CClient(hostname=defs.SSH_HOST, username=defs.SSH_USER, password=defs.SSH_PASSWORD, simulate=defs.sim_mode)
    i2c_client.connect()
    ClockGenTester(chips, i2c_client).run()
    i2c_client.close()
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
