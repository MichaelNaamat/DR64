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
    def __init__(self, chips: list[defs.CChipDef], rem_client: defs.CBaseClient):
        self.chips = chips
        self.rem_client = rem_client

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
        dev_id = self.rem_client.i2c_get(chip.bus, chip.dev, self.REG_DEVICEID, "w")
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
    
    Appl = defs.CApplication(sys.argv)
    Appl.read_args()

    # --->>> Allocate Remote Client according to link type (ssh, telnet, etc.) and connect to the remote host
    match Appl.link:
        case "ssh":
            rem_client = defs.CSSHClient(hostname=Appl.hostname, username=Appl.username, password=Appl.password, simulate=Appl.sim_mode)
        case "serial":
            rem_client = defs.CSerialClient(com=Appl.com, baud=Appl.baud, simulate=Appl.sim_mode)
        case _:
            print(f"{defs.C_RED_B}  >>> ERROR: Unsupported link type '{Appl.link}' specified!{defs.C_NONE}")
            return 1
        
    rem_client.connect()
    PMICTester(chips, rem_client).run()
    rem_client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
