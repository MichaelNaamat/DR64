#!/usr/bin/env python3

import re
import subprocess
import sys
import time
import script_defs as defs

REG_TEMP = "0x00"
REG_CR = "0x01"
REG_TLOW = "0x02"
REG_THIGH = "0x03"
REG_OS = "0x04"

TEMP_CHIPS = [
    {"name": "U60", "bus": "0x04", "dev": "0x48"},
    {"name": "U61", "bus": "0x04", "dev": "0x4C"},
    {"name": "U62", "bus": "0x04", "dev": "0x49"},
    {"name": "U64", "bus": "0x04", "dev": "0x4A"},
    {"name": "U127", "bus": "0x00", "dev": "0x49"},
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
def i2cset(bus, dev, reg, value, mode=None):
    if defs.sim_mode:
        return  
    args = ["i2cset", "-y", "-f", bus, dev, reg, value]
    if mode is not None:
        args.append(mode)
    subprocess.run(args, capture_output=True, text=True, check=True)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def read_gpio_pc04():
    try:
        with open("/sys/kernel/debug/gpio", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return "unknown"

    for line in lines:
        if "PC_04" in line:
            match = re.search(r"\b(?:hi|lo)\b", line)
            if match:
                return match.group(0)
            return "unknown"
    return "unknown"

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def temp75b_check_int(chip_info):
    bus = chip_info["bus"]
    dev = chip_info["dev"]

    org_t_low = i2cget(bus, dev, REG_TLOW, "w")
    org_t_high = i2cget(bus, dev, REG_THIGH, "w")

    print(f"{defs.C_YELLOW_B}")
    print("****************************************************")
    print(f"* Testing Temp Sens {chip_info['name']}: Addr {dev} on i2c bus {bus}")
    print(f"* T-Low={org_t_low}c, T-High={org_t_high}c")
    print("****************************************************")
    print(f"{defs.C_NONE}", end="")
    time.sleep(0.1)

    i2cset(bus, dev, REG_CR, "0x00")

    int_before = read_gpio_pc04()

    i2cset(bus, dev, REG_THIGH, "+5", "w")
    i2cset(bus, dev, REG_TLOW, "+2", "w")

    int_during = read_gpio_pc04()

    t_low = i2cget(bus, dev, REG_TLOW, "w")
    t_high = i2cget(bus, dev, REG_THIGH, "w")

    i2cset(bus, dev, REG_TLOW, org_t_low, "w")
    i2cset(bus, dev, REG_THIGH, org_t_high, "w")

    cur_temp = i2cget(bus, dev, REG_TEMP, "w")
    cur_temp = int(cur_temp, 0) & 0xFF

    int_after = read_gpio_pc04()

    print(
        f"  T-High/T-Low test: Temp={cur_temp}c, T-Low={t_low}c, T-High={t_high}c, Before({int_before}), During({int_during}), After({int_after}) - ",
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


    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def main():
    defs.debug_mode = False
    defs.sim_mode = False
    
    for arg in sys.argv[1:]:
        if arg == "debug":
            defs.debug_mode = True
        elif arg == "sim":
            defs.sim_mode = True

    for chip in TEMP_CHIPS:
        temp75b_check_int(chip)
    return 0


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
if __name__ == "__main__":
    raise SystemExit(main())
