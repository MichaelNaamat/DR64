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

    def __init__(self, chips: list[defs.CChipDef], i2c_client: defs.I2CClient):
        self.chips = chips
        self.i2c_client = i2c_client

    def _print_header(self, chip: defs.CChipDef) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing PMIC {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)
        dev_id = self.i2c_client.get(chip.bus, chip.dev, self.REG_DEVICEID, "w")
        print(f"{defs.C_BLUE_B}  >>> DEBUG: Device ID={dev_id}{defs.C_NONE}")

    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# PMIC Application Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class PMICApplication:
    HOST = "10.0.0.102"      # Replace with your remote Linux IP or hostname
    USER = "root"      # Replace with your remote Linux username
    PASSWORD = ""  # Replace with your remote Linux password

    def __init__(self, argv: list[str]):
        self.argv = argv
        self.chips = [
            defs.CChipDef(name="U54", bus="0x04", dev="0x20"),
            defs.CChipDef(name="U54", bus="0x04", dev="0x21"),
        ]

    def configure_modes(self) -> None:
        defs.debug_mode = False
        defs.sim_mode = False

        for arg in self.argv[1:]:
            if arg == "debug":
                defs.debug_mode = True
            elif arg == "sim":
                defs.sim_mode = True

    def run(self) -> int:
        self.configure_modes()
        i2c_client = defs.I2CClient(hostname=self.HOST, username=self.USER, password=self.PASSWORD, simulate=defs.sim_mode)
        i2c_client.connect()
        PMICTester(self.chips, i2c_client).run()
        i2c_client.close()
        return 0

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main() -> int:
    return PMICApplication(sys.argv).run()


if __name__ == "__main__":
    raise SystemExit(main())
