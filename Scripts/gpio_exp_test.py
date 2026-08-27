#!/usr/bin/env python3

import subprocess
import sys

C_RED = "\033[0;31m"
C_GREEN = "\033[0;32m"
C_YELLOW = "\033[0;33m"
C_BLUE = "\033[0;34m"
C_RED_B = "\033[1;31m"
C_GREEN_B = "\033[1;32m"
C_YELLOW_B = "\033[1;33m"
C_BLUE_B = "\033[1;34m"
C_NONE = "\033[0m"

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


def run_i2cget(bus, dev, reg):
    completed = subprocess.run(["i2cget", "-y", "-f", bus, dev, reg], capture_output=True, text=True, check=True)
    return int(completed.stdout.strip(), 16)


def gpio_check_dev(chip_info):
    bus = chip_info["bus"]
    dev = chip_info["dev"]

    print(f"{C_YELLOW_B}")
    print("*******************************************************")
    print(f"* Testing GPIO {chip_info['name']}: Addr {dev} on i2c bus {bus}")
    print("*******************************************************")
    print(f"{C_NONE}", end="")

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
        print(f"  {C_GREEN_B}OK (0x{inval0:02X}==0x{outval0:02X}){C_NONE}")
    else:
        print(f"  {C_RED_B}FAIL (0x{inval0:02X}!=0x{outval0:02X}){C_NONE}")

    print(f"  Port1: DIN=0x{din1:02X}, DOUT=0x{dout1:02X}, POL=0x{pol1:02X}, CONF=0x{conf1:02X}", end="")
    if inval1 == outval1:
        print(f"  {C_GREEN_B}OK (0x{inval1:02X}==0x{outval1:02X}){C_NONE}")
    else:
        print(f"  {C_RED_B}FAIL (0x{inval1:02X}!=0x{outval1:02X}){C_NONE}")


def main():
    for chip in GPIO_CHIPS:
        gpio_check_dev(chip)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
