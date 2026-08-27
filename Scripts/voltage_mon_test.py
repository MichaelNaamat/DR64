#!/usr/bin/env python3

import json
import subprocess
import sys
import urllib.request

C_RED = "\033[0;31m"
C_GREEN = "\033[0;32m"
C_YELLOW = "\033[0;33m"
C_BLUE = "\033[0;34m"
C_RED_B = "\033[1;31m"
C_GREEN_B = "\033[1;32m"
C_YELLOW_B = "\033[1;33m"
C_BLUE_B = "\033[1;34m"
C_NONE = "\033[0m"


REG_BANK_SEL = "0xF0"
REG_VMON_LVL = ["0x40", "0x41", "0x42", "0x43", "0x44", "0x45", "0x46", "0x47"]

REG_IEN_UVHF = "0x13"
REG_IEN_UVLF = "0x14"
REG_IEN_OVHF = "0x15"
REG_IEN_OVLF = "0x16"
REG_MON_CH_EN = "0x1E"
REG_VRANGE_MULT = "0x1F"

REG_UV_HF = ["0x20", "0x30", "0x40", "0x50", "0x60", "0x70", "0x80", "0x90"]
REG_OV_HF = ["0x21", "0x31", "0x41", "0x51", "0x61", "0x71", "0x81", "0x91"]
REG_UV_LF = ["0x22", "0x32", "0x42", "0x52", "0x62", "0x72", "0x82", "0x92"]
REG_OV_LF = ["0x23", "0x33", "0x43", "0x53", "0x63", "0x73", "0x83", "0x93"]

def channel(name, min_val, typ_val, max_val):
    return {"name": name, "min": min_val, "typ": typ_val, "max": max_val}

U93_CHANNELS = [
    channel("0.875V (core) +2.5% / -3%", 0.84875, 0.875, 0.896875),
    channel("1.8V (PCIE) +/-5%", 1.71, 1.8, 1.89),
    channel("1.8V (IP) +/-3%", 1.746, 1.8, 1.854),
    channel("0.86V (PCIE) +/-5%", 0.817, 0.86, 0.903),
    channel("0.75V (MIPI) +/-5%", 0.7125, 0.75, 0.7875),
    channel("1.05V (DDR) +/-3%", 1.0185, 1.05, 1.0815),
    channel("0.5V (DDR) +/-5%", 0.475, 0.5, 0.525),
    channel("1.8V (Main) +/-5%", 1.71, 1.8, 1.89),
]

U94_CHANNELS = [
    channel("0.875V (core) +2.5% / -3%", 0.84875, 0.875, 0.896875),
    channel("1.8V (PCIE) +/-5%", 1.71, 1.8, 1.89),
    channel("1.8V (IP) +/-3%", 1.746, 1.8, 1.854),
    channel("0.86V (PCIE) +/-5%", 0.817, 0.86, 0.903),
    channel("0.75V (MIPI) +/-5%", 0.7125, 0.75, 0.7875),
    channel("1.05V (DDR) +/-3%", 1.0185, 1.05, 1.0815),
    channel("0.5V (DDR) +/-5%", 0.475, 0.5, 0.525),
    channel("1.8V (Main) +/-5%", 1.71, 1.8, 1.89),
]

U95_CHANNELS = [
    channel("1.1V (USS_12v_M) +/-5%", 1.03835, 1.1, 1.14765),
    channel("5V (5V_CAN) +/-5%", 4.75, 5.0, 5.25),
    channel("1.2V (DES_1v2) +/-5%", 1.14, 1.2, 1.26),
    channel("1.2V (5V_AOLDO_M) +/-5%", 1.12575, 1.185, 1.24425),
    channel("0.8V (DES_0V8) +/-5%", 0.76, 0.8, 0.84),
    channel("3.3V (3V3) +/-5%", 3.135, 3.3, 3.465),
    channel("1.1V (12vPoC_M) +/-5%", 1.03835, 1.1, 1.14765),
    channel("5V", 4.75, 5.0, 5.25),
]

U114_CHANNELS = [
    channel("0.8V () +/-5%", 0.76, 0.8, 0.84),
    channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
    channel("0.8V () +/-5%", 0.76, 0.8, 0.84),
    channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
    channel("0.84V () +/-5%", 0.798, 0.84, 0.882),
    channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
    channel("1.8V (ETH_1v8) +/-5%", 1.71, 1.8, 1.89),
    channel("5V (Main 5V) +/-5%", 4.75, 5.0, 5.25),
]

U148_CHANNELS = [
    channel("0.8V (TDA4_0v8_VDD_CORE) +/-5%", 0.76, 0.8, 0.84),
    channel("0.8V (TDA4_0v8_CPU_AVS) +/-5%", 0.76, 0.8, 0.84),
    channel("1.1V (TDA4_1v1) +/-5%", 1.045, 1.1, 1.155),
    channel("0.85V (TDA4_0v85) +/-5%", 0.8075, 0.85, 0.8925),
    channel("1.8V (TDA4_1v8_PHY_LDO) +/-5%", 1.71, 1.8, 1.89),
    channel("0.8V (TDA4_0v8_DLL_LDO) +/-5%", 0.76, 0.8, 0.84),
    channel("1.8V (TDA4_1v8_PLL_LDO) +/-5%", 1.71, 1.8, 1.89),
    None,
]

VMON_CHIPS = [
    {"name": "U93", "bus": "0x00", "dev": "0x37", "channels": U93_CHANNELS},
    {"name": "U94", "bus": "0x00", "dev": "0x36", "channels": U94_CHANNELS},
    {"name": "U95", "bus": "0x00", "dev": "0x35", "channels": U95_CHANNELS},
    {"name": "U114", "bus": "0x00", "dev": "0x34", "channels": U114_CHANNELS},
]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def run_command(args):
    global sim_mode
    if sim_mode:
        return "0xAA"  # Simulated response
    completed = subprocess.run(args, capture_output=True, text=True, check=True)
    return completed.stdout.strip()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def i2cget(bus, dev, reg):
    return run_command(["i2cget", "-y", "-f", bus, dev, reg])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def i2cset(bus, dev, reg, value):
    run_command(["i2cset", "-y", "-f", bus, dev, reg, value])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def vmon_get_pin(pin):
    global sim_mode
    if sim_mode:
        return "0"  # Simulated response

    payload = json.dumps({"log_level": "INFO", "gpios": [pin]}).encode("utf-8")
    request = urllib.request.Request(
        "http://10.0.0.102:8000/controller/gpio/read_values/",
        data=payload,
        headers={"accept": "application/json", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        body = response.read().decode("utf-8")

    try:
        decoded = json.loads(body)
        if isinstance(decoded, dict):
            data = decoded.get("data", [])
            if data:
                value = data[0].get("Val")
                if value is not None:
                    return str(value)
    except json.JSONDecodeError:
        pass

    return body.strip()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def read_hex_int(bus, dev, reg):
    return int(i2cget(bus, dev, reg), 0)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def format_voltage(raw_value, coef, mul):
    return f"{coef + raw_value * mul:.3f}"


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Print the result of an interrupt test
# Parameters:
# label - Name of the interrupt
# before_state - State before the test
# during_state - State during the test
# after_state - State after the test
# Return: None
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def print_interrupt_result(label, before_state, during_state, after_state):
    print(
        f"  >>> {label} interrupt state: Before({before_state}), During({during_state}), After({after_state}): ",
        end="",
    )
    print(
        f"{C_RED_B}FAIL,{C_NONE}" if before_state == "0" else f"{C_GREEN_B}Pass,{C_NONE}",
        end="",
    )
    print(
        f"{C_RED_B}FAIL,{C_NONE}" if during_state == "1" else f"{C_GREEN_B}Pass,{C_NONE}",
        end="",
    )
    print(
        f"{C_RED_B}FAIL{C_NONE}" if after_state == "0" else f"{C_GREEN_B}Pass{C_NONE}"
    )

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def vmon_check_channel(bus, dev, ch, ch_info, coef, mul, debug_mode):
    min_val = ch_info["min"]
    typ_val = ch_info["typ"]
    max_val = ch_info["max"]

    i2cset(bus, dev, REG_BANK_SEL, "0x00")
    mon_lvl = read_hex_int(bus, dev, REG_VMON_LVL[ch])

    i2cset(bus, dev, REG_BANK_SEL, "0x01")
    uv_hf = read_hex_int(bus, dev, REG_UV_HF[ch])
    ov_hf = read_hex_int(bus, dev, REG_OV_HF[ch])
    uv_lf = read_hex_int(bus, dev, REG_UV_LF[ch])
    ov_lf = read_hex_int(bus, dev, REG_OV_LF[ch])

    if mon_lvl <= 0 or mon_lvl > 255:
        print(f"{C_RED_B}  >>> ERROR: Invalid monitor level ({mon_lvl}) for channel {ch}{C_NONE}")
        return

    if debug_mode:
        mon_lvl_v = format_voltage(mon_lvl, coef, mul)
        uv_hf_v = format_voltage(uv_hf, coef, mul)
        ov_hf_v = format_voltage(ov_hf, coef, mul)
        uv_lf_v = format_voltage(uv_lf, coef, mul)
        ov_lf_v = format_voltage(ov_lf, coef, mul)

        print(
            f"{C_BLUE_B}  >>> DEBUG: Ch {ch}: min={min_val}, typ={typ_val}, max={max_val}, MON_LVL={mon_lvl_v}({mon_lvl})"
        )
        print(
            f"                             UV_HF={uv_hf_v}({uv_hf}) OV_HF={ov_hf_v}({ov_hf}) UV_LF={uv_lf_v}({uv_lf}) OV_LF={ov_lf_v}({ov_lf}){C_NONE}"
        )

        if float(mon_lvl_v) < min_val:
            print(f"{C_RED}  >>> Ch {ch}: ERROR: Less than min ({mon_lvl_v} < {min_val}){C_NONE}")
        elif float(mon_lvl_v) > max_val:
            print(f"{C_RED}  >>> Ch {ch}: ERROR: More than max ({mon_lvl_v} > {max_val}){C_NONE}")
        else:
            print(f"{C_GREEN}  >>> Ch {ch}: OK: {mon_lvl_v} is within range [{min_val}, {max_val}]{C_NONE}")

    int_stat1 = vmon_get_pin("PK_08")

    i2cset(bus, dev, REG_UV_HF[ch], f"0x{ov_hf:02x}")
    int_stat2 = vmon_get_pin("PK_08")

    i2cset(bus, dev, REG_UV_HF[ch], f"0x{uv_hf:02x}")
    int_stat3 = vmon_get_pin("PK_08")

    print_interrupt_result(f"Ch {ch}: UV", int_stat1, int_stat2, int_stat3)

    int_stat1 = vmon_get_pin("PK_08")

    i2cset(bus, dev, REG_OV_HF[ch], f"0x{uv_hf:02x}")
    int_stat2 = vmon_get_pin("PK_08")

    i2cset(bus, dev, REG_OV_HF[ch], f"0x{ov_hf:02x}")
    int_stat3 = vmon_get_pin("PK_08")

    print_interrupt_result(f"Ch {ch}: OV", int_stat1, int_stat2, int_stat3)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def vmon_check_dev(chip_info):
    bus = chip_info["bus"]
    dev = chip_info["dev"]
    chlist = chip_info["channels"]

    i2cset(bus, dev, REG_BANK_SEL, "0x01")
    vrange_mult = read_hex_int(bus, dev, REG_VRANGE_MULT)

    print(C_YELLOW)
    print("****************************************************")
    print(f"* Testing {chip_info['name']}: Addr {dev} on i2c bus {bus} *")
    if debug_mode:
        ien_uvhf = i2cget(bus, dev, REG_IEN_UVHF)
        ien_uvlf = i2cget(bus, dev, REG_IEN_UVLF)
        ien_ovhf = i2cget(bus, dev, REG_IEN_OVHF)
        ien_ovlf = i2cget(bus, dev, REG_IEN_OVLF)
        mon_ch_en = i2cget(bus, dev, REG_MON_CH_EN)
        print(
            f"* Int enable: UVHF={ien_uvhf}, UVLF={ien_uvlf}, OVHF={ien_ovhf}, OVLF={ien_ovlf}, MON_CH_EN={mon_ch_en} *"
        )
    print(f"****************************************************{C_NONE}")

    ch_ind = 0
    for ch_info in chlist:
        if not ch_info or not ch_info.get("name"):
            continue

        if vrange_mult & (1 << ch_ind):
            vmon_check_channel(bus, dev, ch_ind, ch_info, 0.8, 0.020, debug_mode)
        else:
            vmon_check_channel(bus, dev, ch_ind, ch_info, 0.2, 0.005, debug_mode)

        ch_ind += 1


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main entry point for the script
# Parameters:
# argv - Command line arguments
# Return: Exit code
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main(argv):
    global debug_mode
    global sim_mode
    debug_mode = False
    sim_mode = False
    
    for arg in argv[1:]:
        if arg == "debug":
            debug_mode = True
        elif arg == "sim":
            sim_mode = True

    for chip in VMON_CHIPS:
        vmon_check_dev(chip)

    return 0


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
if __name__ == "__main__":
    raise SystemExit(main(sys.argv))