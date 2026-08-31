#!/usr/bin/env python3

import subprocess
import sys
from dataclasses import dataclass
from typing import List

import script_defs as defs

@dataclass(frozen=False)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Power Supply Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class PowerSupplyTester:
    REG_VSET = "0x00"
    REG_CONTROL1 = "0x01"
    REG_CONTROL2 = "0x02"
    REG_CONTROL3 = "0x03"
    REG_STATUS = "0x04"

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, chips: List[defs.CChipDef], ssh_client: defs.CSSHClient):
        self.chips = chips
        self.ssh_client = ssh_client

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _print_header(self, chip: defs.CChipDef) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("*******************************************************")
        print(f"* Testing Power Supply {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)

        vset = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_VSET, "w")
        control1 = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_CONTROL1, "w")
        control2 = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_CONTROL2, "w")
        control3 = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_CONTROL3, "w")
        status   = self.ssh_client.i2c_get(chip.bus, chip.dev, self.REG_STATUS, "w")

        print(
            f"{defs.C_BLUE_B}  >>> DEBUG: VSET={vset}, Control1={control1}, "
            f"Control2={control2}, Control3={control3}, Status={status}{defs.C_NONE}"
        )

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
    defs.configure_modes(sys.argv)
    ssh_client = defs.CSSHClient(hostname=defs.SSH_HOST, username=defs.SSH_USER, password=defs.SSH_PASSWORD, simulate=defs.sim_mode)
    ssh_client.connect()
    PowerSupplyTester(chips, ssh_client).run()
    ssh_client.close()
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
