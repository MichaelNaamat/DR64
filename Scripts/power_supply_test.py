#!/usr/bin/env python3

import subprocess

C_YELLOW_B = "\033[1;33m"
C_BLUE_B = "\033[1;34m"
C_NONE = "\033[0m"

REG_PS_VSET = "0x00"
REG_PS_CONTROL1 = "0x01"
REG_PS_CONTROL2 = "0x02"
REG_PS_CONTROL3 = "0x03"
REG_PS_STATUS = "0x04"

PS_CHIPS = [
    {"name": "U33", "bus": "0x01", "dev": "0x33"},
    {"name": "A_U26", "bus": "0x01", "dev": "0x40"},
    {"name": "A_U18", "bus": "0x01", "dev": "0x43"},
    {"name": "A_U100", "bus": "0x01", "dev": "0x46"},
    {"name": "U32", "bus": "0x02", "dev": "0x30"},
    {"name": "B_U26", "bus": "0x02", "dev": "0x40"},
    {"name": "U34", "bus": "0x02", "dev": "0x43"},
    {"name": "B_U100", "bus": "0x02", "dev": "0x46"},
]


def i2cget(bus, dev, reg):
    completed = subprocess.run(["i2cget", "-y", "-f", bus, dev, reg], capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def ps_check_dev(chip_info):
    bus = chip_info["bus"]
    dev = chip_info["dev"]

    print(f"{C_YELLOW_B}")
    print("*******************************************************")
    print(f"* Testing Power Supply {chip_info['name']}: Addr {dev} on i2c bus {bus}")
    print("*******************************************************")
    print(f"{C_NONE}", end="")

    vset = i2cget(bus, dev, REG_PS_VSET)
    control1 = i2cget(bus, dev, REG_PS_CONTROL1)
    control2 = i2cget(bus, dev, REG_PS_CONTROL2)
    control3 = i2cget(bus, dev, REG_PS_CONTROL3)
    status = i2cget(bus, dev, REG_PS_STATUS)
    print(f"{C_BLUE_B}  >>> DEBUG: VSET={vset}, Control1={control1}, Control2={control2}, Control3={control3}, Status={status}{C_NONE}")


def main():
    for chip in PS_CHIPS:
        ps_check_dev(chip)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
