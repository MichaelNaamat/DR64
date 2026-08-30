#!/usr/bin/env python3

import subprocess
import sys
from dataclasses import dataclass
from typing import List

import script_defs as defs

@dataclass(frozen=True)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Power Supply Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class PowerSupplyTester:
    REG_VSET = "0x00"
    REG_CONTROL1 = "0x01"
    REG_CONTROL2 = "0x02"
    REG_CONTROL3 = "0x03"
    REG_STATUS = "0x04"

    def __init__(self, chips: List[defs.CChipDef], i2c_client: defs.I2CClient):
        self.chips = chips
        self.i2c_client = i2c_client

    def _print_header(self, chip: defs.CChipDef) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing Power Supply {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)

        vset = self.i2c_client.get(chip.bus, chip.dev, self.REG_VSET)
        control1 = self.i2c_client.get(chip.bus, chip.dev, self.REG_CONTROL1)
        control2 = self.i2c_client.get(chip.bus, chip.dev, self.REG_CONTROL2)
        control3 = self.i2c_client.get(chip.bus, chip.dev, self.REG_CONTROL3)
        status   = self.i2c_client.get(chip.bus, chip.dev, self.REG_STATUS)

        print(
            f"{defs.C_BLUE_B}  >>> DEBUG: VSET={vset}, Control1={control1}, "
            f"Control2={control2}, Control3={control3}, Status={status}{defs.C_NONE}"
        )

    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Power Supply Application Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class PowerSupplyApplication:
    def __init__(self, argv: List[str]):
        self.argv = argv
        self.chips = [
            defs.CChipDef(name="U33"   , bus="0x01", dev="0x33"),
            defs.CChipDef(name="A_U26" , bus="0x01", dev="0x40"),
            defs.CChipDef(name="A_U18" , bus="0x01", dev="0x43"),
            defs.CChipDef(name="A_U100", bus="0x01", dev="0x46"),
            defs.CChipDef(name="U32"   , bus="0x02", dev="0x30"),
            defs.CChipDef(name="B_U26" , bus="0x02", dev="0x40"),
            defs.CChipDef(name="U34"   , bus="0x02", dev="0x43"),
            defs.CChipDef(name="B_U100", bus="0x02", dev="0x46"),
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
        i2c_client = defs.I2CClient(simulate=defs.sim_mode)
        PowerSupplyTester(self.chips, i2c_client).run()
        return 0


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-  
def main() -> int:
    return PowerSupplyApplication(sys.argv).run()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
