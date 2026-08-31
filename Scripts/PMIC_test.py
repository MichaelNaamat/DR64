#!/usr/bin/env python3

import sys
from dataclasses import dataclass

import script_defs as defs

@dataclass(frozen=False)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# PMIC Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class PMICTester:
    REG_DEVICEID = "0x2B"

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, chips: list[defs.CChipDef], i2c_client: defs.I2CClient):
        self.chips = chips
        self.i2c_client = i2c_client

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _print_header(self, chip: defs.CChipDef) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing PMIC {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)
        dev_id = self.i2c_client.get(chip.bus, chip.dev, self.REG_DEVICEID, "w")
        print(f"{defs.C_BLUE_B}  >>> DEBUG: Device ID={dev_id}{defs.C_NONE}")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main() -> int:
    chips = [
        defs.CChipDef(name="U54", bus="0x04", dev="0x20"),
        defs.CChipDef(name="U54", bus="0x04", dev="0x21"),
    ]
    defs.configure_modes(sys.argv)

    i2c_client = defs.I2CClient(hostname=defs.SSH_HOST, username=defs.SSH_USER, password=defs.SSH_PASSWORD, simulate=defs.sim_mode)
    i2c_client.connect()
    PMICTester(chips, i2c_client).run()
    i2c_client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
