#!/usr/bin/env python3

import subprocess

C_YELLOW_B = "\033[1;33m"
C_BLUE_B = "\033[1;34m"
C_NONE = "\033[0m"

REG_CLK_DEVICE_PN_BASE = "0x0D"
REG_CLK_DEVICE_REV = "0x0E"

CLOCK_GEN_CHIPS = [
    {"name": "U87", "bus": "0x01", "dev": "0x6A"},
    {"name": "U88", "bus": "0x01", "dev": "0x6B"},
]


def i2cget(bus, dev, reg, mode=None):
    args = ["i2cget", "-y", "-f", bus, dev, reg]
    if mode is not None:
        args.append(mode)
    completed = subprocess.run(args, capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def clock_gen_check_dev(chip_info):
    bus = chip_info["bus"]
    dev = chip_info["dev"]

    print(f"{C_YELLOW_B}")
    print("*******************************************************")
    print(f"* Testing Clock-Gen {chip_info['name']}: Addr {dev} on i2c bus {bus}")
    print("*******************************************************")
    print(f"{C_NONE}", end="")

    dev_pn = i2cget(bus, dev, REG_CLK_DEVICE_PN_BASE)
    dev_rev = i2cget(bus, dev, REG_CLK_DEVICE_REV)
    print(f"{C_BLUE_B}  >>> DEBUG: Device PN={dev_pn}, Device REV={dev_rev}{C_NONE}")


def main():
    for chip in CLOCK_GEN_CHIPS:
        clock_gen_check_dev(chip)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
