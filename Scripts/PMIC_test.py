#!/usr/bin/env python3

import subprocess
import sys
from dataclasses import dataclass

import script_defs as defs


@dataclass(frozen=True)

# --->>> PMIC Chip Definition
class PmicChip:
    name: str
    bus: str
    dev: str

# --->>> I2C Client Definition
class I2CClient:
    def __init__(self, simulate: bool = False):
        self.simulate = simulate

    # --->>> I2C Get Method to read byte/word register from the device via I2C bus
    def get(self, bus: str, dev: str, reg: str, mode: str | None = None) -> str:
        if self.simulate:
            return "0x00"

        args = ["i2cget", "-y", "-f", bus, dev, reg]
        if mode is not None:
            args.append(mode)

        completed = subprocess.run(args, capture_output=True, text=True, check=True)
        return completed.stdout.strip()
    
    # --->>> I2C Set Method to write byte/word register to the device via I2C bus
    def set(self, bus: str, dev: str, reg: str, value: str, mode: str | None = None) -> None:
        if self.simulate:
            return

        args = ["i2cset", "-y", "-f", bus, dev, reg, value]
        if mode is not None:
            args.append(mode)

        subprocess.run(args, capture_output=True, text=True, check=True)
        
# --->>> PMIC Tester Class Definition
class PMICTester:
    REG_PMIC_DEVICEID = "0x2B"

    def __init__(self, chips: list[PmicChip], i2c_client: I2CClient):
        self.chips = chips
        self.i2c_client = i2c_client

    def _print_header(self, chip: PmicChip) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing PMIC {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    def check_device(self, chip: PmicChip) -> None:
        self._print_header(chip)
        dev_id = self.i2c_client.get(chip.bus, chip.dev, self.REG_PMIC_DEVICEID, "w")
        print(f"{defs.C_BLUE_B}  >>> DEBUG: Device ID={dev_id}{defs.C_NONE}")

    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# --->>> PMIC Application Class Definition
class PMICApplication:
    def __init__(self, argv: list[str]):
        self.argv = argv
        self.chips = [
            PmicChip(name="U54", bus="0x04", dev="0x20"),
            PmicChip(name="U54", bus="0x04", dev="0x21"),
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
        i2c_client = I2CClient(simulate=defs.sim_mode)
        PMICTester(self.chips, i2c_client).run()
        return 0

# --->>> Main Entry Point
def main() -> int:
    return PMICApplication(sys.argv).run()


if __name__ == "__main__":
    raise SystemExit(main())
