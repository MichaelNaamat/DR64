#!/usr/bin/env python3

import subprocess
import sys
import script_defs as defs

REG_GPIO_DIN0 = "0x00"
REG_GPIO_DIN1 = "0x01"
REG_GPIO_DOUT0 = "0x02"
REG_GPIO_DOUT1 = "0x03"
REG_GPIO_POL0 = "0x04"
REG_GPIO_POL1 = "0x05"
REG_GPIO_CONF0 = "0x06"
REG_GPIO_CONF1 = "0x07"

GPIO_CHIPS = [
    {"name": "U103", "bus": "0x04", "dev": "0x74"},
    {"name": "U104", "bus": "0x00", "dev": "0x75"},
    {"name": "U146", "bus": "0x00", "dev": "0x74"},
]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def run_i2cget(bus, dev, reg):
    if defs.sim_mode:
        return 0x00
    completed = subprocess.run(["i2cget", "-y", "-f", bus, dev, reg], capture_output=True, text=True, check=True)
    return int(completed.stdout.strip(), 16)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def gpio_check_dev(chip_info):
    bus = chip_info["bus"]
    dev = chip_info["dev"]

    print(f"{defs.C_YELLOW_B}")
    print("*******************************************************")
    print(f"* Testing GPIO {chip_info['name']}: Addr {dev} on i2c bus {bus}")
    print("*******************************************************")
    print(f"{defs.C_NONE}", end="")

    din0 = run_i2cget(bus, dev, REG_GPIO_DIN0)
    din1 = run_i2cget(bus, dev, REG_GPIO_DIN1)
    dout0 = run_i2cget(bus, dev, REG_GPIO_DOUT0)
    dout1 = run_i2cget(bus, dev, REG_GPIO_DOUT1)
    pol0 = run_i2cget(bus, dev, REG_GPIO_POL0)
    pol1 = run_i2cget(bus, dev, REG_GPIO_POL1)
    conf0 = run_i2cget(bus, dev, REG_GPIO_CONF0)
    conf1 = run_i2cget(bus, dev, REG_GPIO_CONF1)

    outval0 = dout0 & ~conf0
    inval0 = din0 & ~conf0
    outval1 = dout1 & ~conf1
    inval1 = din1 & ~conf1

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

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def main():
    defs.debug_mode = False
    defs.sim_mode = False
    
    for arg in sys.argv[1:]:
        if arg == "debug":
            defs.debug_mode = True
        elif arg == "sim":
            defs.sim_mode = True

    for chip in GPIO_CHIPS:
        gpio_check_dev(chip)
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
