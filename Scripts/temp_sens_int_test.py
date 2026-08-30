#!/usr/bin/env python3

import re
import subprocess
from dataclasses import dataclass
import sys
import time
from typing import List, Optional

import script_defs as defs

@dataclass(frozen=True)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Temperature Sensor Interrupt Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class TempSensorInterruptTester:
    REG_TEMP = "0x00"
    REG_CR = "0x01"
    REG_TLOW = "0x02"
    REG_THIGH = "0x03"
    REG_OS = "0x04"

    def __init__(self, chips: List[defs.CChipDef], i2c_client: defs.I2CClient, gpio_reader: defs.GPIOReader):
        self.chips = chips
        self.i2c_client = i2c_client
        self.gpio_reader = gpio_reader

    def _print_header(self, chip: defs.CChipDef, t_low: str, t_high: str) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("****************************************************")
        print(f"* Testing Temp Sens {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print(f"* T-Low={t_low}c, T-High={t_high}c")
        print("****************************************************")
        print(f"{defs.C_NONE}", end="")

    def check_interrupt(self, chip: defs.CChipDef) -> None:
        org_t_low = self.i2c_client.get(chip.bus, chip.dev, self.REG_TLOW, "w")
        org_t_high = self.i2c_client.get(chip.bus, chip.dev, self.REG_THIGH, "w")

        self._print_header(chip, org_t_low, org_t_high)
        time.sleep(0.1)

        self.i2c_client.set(chip.bus, chip.dev, self.REG_CR, "0x00")

        int_before = self.gpio_reader.read("PC_04")

        self.i2c_client.set(chip.bus, chip.dev, self.REG_THIGH, "+5", "w")
        self.i2c_client.set(chip.bus, chip.dev, self.REG_TLOW, "+2", "w")

        int_during = self.gpio_reader.read("PC_04")

        t_low = self.i2c_client.get(chip.bus, chip.dev, self.REG_TLOW, "w")
        t_high = self.i2c_client.get(chip.bus, chip.dev, self.REG_THIGH, "w")

        self.i2c_client.set(chip.bus, chip.dev, self.REG_TLOW, org_t_low, "w")
        self.i2c_client.set(chip.bus, chip.dev, self.REG_THIGH, org_t_high, "w")

        cur_temp = self.i2c_client.get(chip.bus, chip.dev, self.REG_TEMP, "w")
        cur_temp = int(cur_temp, 0) & 0xFF

        int_after = self.gpio_reader.read("PC_04")

        print(
            f"  T-High/T-Low test: Temp={cur_temp}c, T-Low={t_low}c, T-High={t_high}c, "
            f"Before({int_before}), During({int_during}), After({int_after}) - ",
            end="",
        )

        ok_before = int_before == "hi"
        ok_during = int_during == "lo"
        ok_after = int_after == "hi"

        if ok_before:
            print(f"{defs.C_GREEN_B}Pass,{defs.C_NONE}", end="")
        else:
            print(f"{defs.C_RED_B}FAIL,{defs.C_NONE}", end="")

        if ok_during:
            print(f"{defs.C_GREEN_B}Pass,{defs.C_NONE}", end="")
        else:
            print(f"{defs.C_RED_B}FAIL,{defs.C_NONE}", end="")

        if ok_after:
            print(f"{defs.C_GREEN_B}Pass{defs.C_NONE}")
        else:
            print(f"{defs.C_RED_B}FAIL{defs.C_NONE}")

    def run(self) -> None:
        for chip in self.chips:
            self.check_interrupt(chip)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main():
    defs.debug_mode = False
    defs.sim_mode = False

    for arg in sys.argv[1:]:
        if arg == "debug":
            defs.debug_mode = True
        elif arg == "sim":
            defs.sim_mode = True

    chips = [
        defs.CChipDef(name="U60", bus="0x04", dev="0x48"),
        defs.CChipDef(name="U61", bus="0x04", dev="0x4C"),
        defs.CChipDef(name="U62", bus="0x04", dev="0x49"),
        defs.CChipDef(name="U64", bus="0x04", dev="0x4A"),
        defs.CChipDef(name="U127", bus="0x00", dev="0x49"),
    ]

    i2c_client = defs.I2CClient(simulate=defs.sim_mode)
    gpio_reader = defs.CGPIOReader()
    defs.TempSensorInterruptTester(chips, i2c_client, gpio_reader).run()
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
