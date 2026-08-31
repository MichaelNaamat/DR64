#!/usr/bin/env python3

import re
import subprocess
from dataclasses import dataclass
import sys
import time
from typing import List, Optional

import script_defs as defs

@dataclass(frozen=False)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Temperature Sensor Interrupt Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class TempSensorInterruptTester:
    REG_TEMP = "0x00"
    REG_CR = "0x01"
    REG_TLOW = "0x02"
    REG_THIGH = "0x03"
    REG_OS = "0x04"

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, chips: List[defs.CChipDef], ssh_client: defs.CSSHClient):
        self.chips = chips
        self.ssh_client = ssh_client

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _print_header(self, chip: defs.CChipDef, t_low: str, t_high: str) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("****************************************************")
        print(f"* Testing Temp Sens {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print(f"* T-Low={t_low}c, T-High={t_high}c")
        print("****************************************************")
        print(f"{defs.C_NONE}", end="")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_interrupt(self, chip: defs.CChipDef) -> None:
        org_t_low = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_TLOW, "w")
        org_t_high = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_THIGH, "w")

        self._print_header(chip, org_t_low, org_t_high)
        time.sleep(0.1)

        self.ssh_client.i2c_set(chip.bus, chip.dev, self.REG_CR, "0x00")

        int_before = self.ssh_client.gpio_read("PC_04")

        self.ssh_client.i2c_set(chip.bus, chip.dev, self.REG_THIGH, "+5", "w")
        self.ssh_client.i2c_set(chip.bus, chip.dev, self.REG_TLOW, "+2", "w")

        int_during = self.ssh_client.gpio_read("PC_04")

        t_low = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_TLOW, "w")
        t_high = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_THIGH, "w")

        self.ssh_client.i2c_set(chip.bus, chip.dev, self.REG_TLOW, org_t_low, "w")
        self.ssh_client.i2c_set(chip.bus, chip.dev, self.REG_THIGH, org_t_high, "w")

        cur_temp = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_TEMP, "w")
        cur_temp = int(cur_temp, 0) & 0xFF

        int_after = self.ssh_client.gpio_read("PC_04")

        print(
            f"  T-High/T-Low test: Temp={cur_temp}c, T-Low={t_low}c, T-High={t_high}c, "
            f"Before({int_before}), During({int_during}), After({int_after}) - ",
            end="",
        )

        if int_before == "hi":
            print(f"{defs.C_GREEN_B}Pass,{defs.C_NONE}", end="")
        else:
            print(f"{defs.C_RED_B}FAIL,{defs.C_NONE}", end="")

        if int_during == "lo":
            print(f"{defs.C_GREEN_B}Pass,{defs.C_NONE}", end="")
        else:
            print(f"{defs.C_RED_B}FAIL,{defs.C_NONE}", end="")

        if int_after == "hi":
            print(f"{defs.C_GREEN_B}Pass{defs.C_NONE}")
        else:
            print(f"{defs.C_RED_B}FAIL{defs.C_NONE}")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_interrupt(chip)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main():
    chips = [
        defs.CChipDef(name="U60" , bus="0x04", dev="0x48"),
        defs.CChipDef(name="U61" , bus="0x04", dev="0x4C"),
        defs.CChipDef(name="U62" , bus="0x04", dev="0x49"),
        defs.CChipDef(name="U64" , bus="0x04", dev="0x4A"),
        defs.CChipDef(name="U127", bus="0x00", dev="0x49"),
    ]

    defs.configure_modes(sys.argv)
    ssh_client = defs.CSSHClient(hostname=defs.SSH_HOST, username=defs.SSH_USER, password=defs.SSH_PASSWORD, simulate=defs.sim_mode)
    ssh_client.connect()
    TempSensorInterruptTester(chips, ssh_client).run()
    ssh_client.close()
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
