#!/usr/bin/env python3

import subprocess
import sys
import script_defs as defs

REG_PMIC_DEVICEID = "0x2B"

PMIC_CHIPS = [
    {"name": "U54", "bus": "0x04", "dev": "0x20"},
    {"name": "U54", "bus": "0x04", "dev": "0x21"},
]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def i2cget(bus, dev, reg, mode=None):
    if defs.sim_mode:
        return "0x00"
    args = ["i2cget", "-y", "-f", bus, dev, reg]
    if mode is not None:
        args.append(mode)
    completed = subprocess.run(args, capture_output=True, text=True, check=True)
    return completed.stdout.strip()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def pmic_check_dev(chip_info):
    bus = chip_info["bus"]
    dev = chip_info["dev"]

    print(f"{defs.C_YELLOW_B}")
    print("*******************************************************")
    print(f"* Testing PMIC {chip_info['name']}: Addr {dev} on i2c bus {bus}")
    print("*******************************************************")
    print(f"{defs.C_NONE}", end="")

    dev_id = i2cget(bus, dev, REG_PMIC_DEVICEID, "w")
    print(f"{defs.C_BLUE_B}  >>> DEBUG: Device ID={dev_id}{defs.C_NONE}")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def main():
    defs.debug_mode = False
    defs.sim_mode = False
    
    for arg in sys.argv[1:]:
        if arg == "debug":
            defs.debug_mode = True
        elif arg == "sim":
            defs.sim_mode = True

    for chip in PMIC_CHIPS:
        pmic_check_dev(chip)
    return 0
    
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
if __name__ == "__main__":
    raise SystemExit(main())
