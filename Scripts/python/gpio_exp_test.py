#!/usr/bin/env python3

import subprocess
import sys
from typing import List

import script_defs as defs
from dataclasses import dataclass
@dataclass(frozen=False)

# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# GPIO Expander Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class GPIOExpanderTester:
    REG_DIN0 = "0x00"
    REG_DIN1 = "0x01"
    REG_DOUT0 = "0x02"
    REG_DOUT1 = "0x03"
    REG_POL0 = "0x04"
    REG_POL1 = "0x05"
    REG_CONF0 = "0x06"
    REG_CONF1 = "0x07"

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Constructor Method to initialize the GPIOExpanderTester 
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
        print(f"* Testing GPIO {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print("*******************************************************")
        print(f"{defs.C_NONE}", end="")

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Read Ports Method to read the input, output, polarity, 
    # and configuration registers from the chip
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _read_ports(self, chip: defs.CChipDef) -> tuple[int, int, int, int, int, int, int, int]:
        din0 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_DIN0)
        din1 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_DIN1)
        dout0 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_DOUT0)
        dout1 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_DOUT1)
        pol0 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_POL0)
        pol1 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_POL1)
        conf0 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_CONF0)
        conf1 = self.ssh_client.i2c_get_int(chip.bus, chip.dev, self.REG_CONF1)
        return din0, din1, dout0, dout1, pol0, pol1, conf0, conf1

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Check Device Method to verify the functionality of the 
    # GPIO expander
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_device(self, chip: defs.CChipDef) -> None:
        self._print_header(chip)

        din0, din1, dout0, dout1, pol0, pol1, conf0, conf1 = self._read_ports(chip)

        outval0 = dout0 & ~conf0
        inval0 = din0 & ~conf0
        outval1 = dout1 & ~conf1
        inval1 = din1 & ~conf1

        # --->>>> Flip signal defined in polarity inversion
        inval0 ^= pol0
        outval0 ^= pol0
        inval1 ^= pol1
        outval1 ^= pol1

        print(f"  Port0: DIN=0x{din0:02X}, DOUT=0x{dout0:02X}, POL=0x{pol0:02X}, CONF=0x{conf0:02X}", end="")
        if inval0 == outval0:
            print(f"  {defs.C_GREEN_B}OK (0x{inval0:02X}==0x{outval0:02X}){defs.C_NONE}")
        else:
            print(f"  {defs.C_RED_B}FAIL (0x{inval0:02X}!=0x{outval0:02X}){defs.C_NONE}")

        print(f"  Port1: DIN=0x{din1:02X}, DOUT=0x{dout1:02X}, POL=0x{pol1:02X}, CONF=0x{conf1:02X}", end="")
        if inval1 == outval1:
            print(f"  {defs.C_GREEN_B}OK (0x{inval1:02X}==0x{outval1:02X}){defs.C_NONE}")
        else:
            print(f"  {defs.C_RED_B}FAIL (0x{inval1:02X}!=0x{outval1:02X}){defs.C_NONE}")

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main() -> int:
    chips = [
        defs.CChipDef(name="U103", bus="0x04", dev="0x74"),
        defs.CChipDef(name="U104", bus="0x00", dev="0x75"),
        defs.CChipDef(name="U146", bus="0x00", dev="0x74"),
    ]
    Appl = defs.CApplication(sys.argv)
    rem_client = Appl.create_remote_client()
    rem_client.connect()
    GPIOExpanderTester(chips, rem_client).run()
    rem_client.close()
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
