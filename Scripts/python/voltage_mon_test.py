#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import List, Optional

import script_defs as defs

@dataclass(frozen=True)
class VoltageChannel:
    name: str
    min_val: float
    typ_val: float
    max_val: float
    pos_percent: float
    neg_percent: float

@dataclass(frozen=False)
# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# Voltage Monitor Chip Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class VoltageMonitorChip:
    name: str
    bus: str
    dev: str
    channels: List[Optional[VoltageChannel]]

def channel(name: str, min_val: float, typ_val: float, max_val: float, pos_percent: float = 5.0, neg_percent: float = 5.0) -> VoltageChannel:
    return VoltageChannel(name=name, min_val=min_val, typ_val=typ_val, max_val=max_val, pos_percent=pos_percent, neg_percent=neg_percent)

# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# Voltage Monitor Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class VoltageMonitorTester:
    REG_BANK_SEL = "0xF0"
    REG_IEN_UVHF = "0x13"
    REG_IEN_UVLF = "0x14"
    REG_IEN_OVHF = "0x15"
    REG_IEN_OVLF = "0x16"
    REG_MON_CH_EN = "0x1E"
    REG_VRANGE_MULT = "0x1F"

    # --->>> Register addresses for voltage monitoring channels
    REG_VMON_LVL = ["0x40", "0x41", "0x42", "0x43", "0x44", "0x45", "0x46", "0x47"]
    REG_UV_HF    = ["0x20", "0x30", "0x40", "0x50", "0x60", "0x70", "0x80", "0x90"]
    REG_OV_HF    = ["0x21", "0x31", "0x41", "0x51", "0x61", "0x71", "0x81", "0x91"]
    REG_UV_LF    = ["0x22", "0x32", "0x42", "0x52", "0x62", "0x72", "0x82", "0x92"]
    REG_OV_LF    = ["0x23", "0x33", "0x43", "0x53", "0x63", "0x73", "0x83", "0x93"]

    # --->>> List of voltage monitor chips to be tested
    u93_channels: List[Optional[VoltageChannel]] = [
        channel("0.875V (core) +2.5% / -3%", 0.84875, 0.875, 0.896875, 2.5, 3.0),
        channel("1.8V (PCIE) +/-5%", 1.71, 1.8, 1.89),
        channel("1.8V (IP) +/-3%", 1.746, 1.8, 1.854, 3.0, 3.0),
        channel("0.86V (PCIE) +/-5%", 0.817, 0.86, 0.903),
        channel("0.75V (MIPI) +/-5%", 0.7125, 0.75, 0.7875),
        channel("1.05V (DDR) +/-3%", 1.0185, 1.05, 1.0815, 3.0, 3.0),
        channel("0.5V (DDR) +/-5%", 0.475, 0.5, 0.525),
        channel("1.8V (Main) +/-5%", 1.71, 1.8, 1.89),
    ]

    u94_channels: List[Optional[VoltageChannel]] = [
        channel("0.875V (core) +2.5% / -3%", 0.84875, 0.875, 0.896875, 2.5, 3.0),
        channel("1.8V (PCIE) +/-5%", 1.71, 1.8, 1.89),
        channel("1.8V (IP) +/-3%", 1.746, 1.8, 1.854, 3.0, 3.0),
        channel("0.86V (PCIE) +/-5%", 0.817, 0.86, 0.903),
        channel("0.75V (MIPI) +/-5%", 0.7125, 0.75, 0.7875),
        channel("1.05V (DDR) +/-3%", 1.0185, 1.05, 1.0815, 3.0, 3.0),
        channel("0.5V (DDR) +/-5%", 0.475, 0.5, 0.525),
        channel("1.8V (Main) +/-5%", 1.71, 1.8, 1.89),
    ]

    u95_channels: List[Optional[VoltageChannel]] = [
        channel("1.1V (USS_12v_M) +/-5%", 1.03835, 1.1, 1.14765),
        channel("5V (5V_CAN) +/-5%", 4.75, 5.0, 5.25),
        channel("1.2V (DES_1v2) +/-5%", 1.14, 1.2, 1.26),
        channel("1.2V (5V_AOLDO_M) +/-5%", 1.12575, 1.185, 1.24425),
        channel("0.8V (DES_0V8) +/-5%", 0.76, 0.8, 0.84),
        channel("3.3V (3V3) +/-5%", 3.135, 3.3, 3.465),
        channel("1.1V (12vPoC_M) +/-5%", 1.03835, 1.1, 1.14765),
        channel("5V", 4.75, 5.0, 5.25),
    ]

    u114_channels: List[Optional[VoltageChannel]] = [
        channel("0.8V () +/-5%", 0.76, 0.8, 0.84),
        channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
        channel("0.8V () +/-5%", 0.76, 0.8, 0.84),
        channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
        channel("0.84V () +/-5%", 0.798, 0.84, 0.882),
        channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
        channel("1.8V (ETH_1v8) +/-5%", 1.71, 1.8, 1.89),
        channel("5V (Main 5V) +/-5%", 4.75, 5.0, 5.25),
    ]

    u148_channels: List[Optional[VoltageChannel]] = [   # TBD....
        channel("0.8V () +/-5%", 0.76, 0.8, 0.84),
        channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
        channel("0.8V () +/-5%", 0.76, 0.8, 0.84),
        channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
        channel("0.84V () +/-5%", 0.798, 0.84, 0.882),
        channel("1.2V () +/-5%", 1.14, 1.2, 1.26),
        channel("1.8V (ETH_1v8) +/-5%", 1.71, 1.8, 1.89),
        channel("5V (Main 5V) +/-5%", 4.75, 5.0, 5.25),
    ]

    chips = [
        VoltageMonitorChip(name="U93" , bus="0x00", dev="0x37", channels=u93_channels),
        VoltageMonitorChip(name="U94" , bus="0x00", dev="0x36", channels=u94_channels),
        VoltageMonitorChip(name="U95" , bus="0x00", dev="0x35", channels=u95_channels),
        VoltageMonitorChip(name="U114", bus="0x00", dev="0x34", channels=u114_channels),
## TBD ??        VoltageMonitorChip(name="U148", bus="0x04", dev="0x33", channels=u148_channels),
    ]

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Constructor Method to initialize the VoltageMonitorTester
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, ssh_client: defs.CBaseClient, debug_mode: bool):
        self.ssh_client = ssh_client
        self.debug_mode = True # debug_mode

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Print Header Method to display a header for the chip
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    @staticmethod
    def print_interrupt_result(label: str, before_state: str, during_state: str, after_state: str) -> None:
        print(
            f"  >>> {label} interrupt state: Before({before_state}), During({during_state}), After({after_state}): ",
            end="",
        )
        print(
            f"{defs.C_GREEN_B}Pass,{defs.C_NONE}" if before_state == "hi" else f"{defs.C_RED_B}FAIL,{defs.C_NONE}",
            end="",
        )
        print(
            f"{defs.C_GREEN_B}Pass,{defs.C_NONE}" if during_state == "lo" else f"{defs.C_RED_B}FAIL,{defs.C_NONE}",
            end="",
        )
        print(
            f"{defs.C_GREEN_B}Pass,{defs.C_NONE}" if after_state == "hi" else f"{defs.C_RED_B}FAIL,{defs.C_NONE}",
            end="\n",)

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Format Voltage Method to format the raw voltage value 
    # with a coefficient and multiplier
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    @staticmethod
    def format_voltage(raw_value: int, coef: float, mul: float) -> float:
        return coef + raw_value * mul

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Check Channel Method to test the functionality of a 
    # voltage monitor channel
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_channel(self, bus: str, dev: str, ch: int, ch_info: VoltageChannel, coef: float, mul: float) -> None:
        min_val = ch_info.min_val
        typ_val = ch_info.typ_val
        max_val = ch_info.max_val
        pos_tolerance = (max_val - min_val) * (ch_info.pos_percent / 100)
        neg_tolerance = (max_val - min_val) * (ch_info.neg_percent / 100)

        self.ssh_client.i2c_set(bus, dev, self.REG_BANK_SEL, "0x00")        # Switch to bank 0 for VMON_LVL register
        mon_lvl = self.ssh_client.i2c_get_int(bus, dev, self.REG_VMON_LVL[ch])

        self.ssh_client.i2c_set(bus, dev, self.REG_BANK_SEL, "0x01")        # Switch to bank 1 for UV/OV registers
        uv_hf = self.ssh_client.i2c_get_int(bus, dev, self.REG_UV_HF[ch])
        ov_hf = self.ssh_client.i2c_get_int(bus, dev, self.REG_OV_HF[ch])
        uv_lf = self.ssh_client.i2c_get_int(bus, dev, self.REG_UV_LF[ch])
        ov_lf = self.ssh_client.i2c_get_int(bus, dev, self.REG_OV_LF[ch])

        if mon_lvl <= 0 or mon_lvl > 255:
            print(f"{defs.C_RED_B}  >>> ERROR: Invalid monitor level ({mon_lvl}) for channel {ch}{defs.C_NONE}")
            return

        if self.debug_mode:
            mon_lvl_v = self.format_voltage(mon_lvl, coef, mul)
            uv_hf_v = self.format_voltage(uv_hf, coef, mul)
            ov_hf_v = self.format_voltage(ov_hf, coef, mul)
            uv_lf_v = self.format_voltage(uv_lf, coef, mul)
            ov_lf_v = self.format_voltage(ov_lf, coef, mul)

            print(
                f"{defs.C_BLUE_B}  >>> DEBUG: Ch {ch}: min={min_val}, typ={typ_val}, max={max_val}, MON_LVL={mon_lvl_v}({mon_lvl})"
            )
            print(
                f"                             UV_HF={uv_hf_v}({uv_hf}) OV_HF={ov_hf_v}({ov_hf}) UV_LF={uv_lf_v}({uv_lf}) OV_LF={ov_lf_v}({ov_lf}){defs.C_NONE}"
            )

            if mon_lvl_v < (min_val - neg_tolerance):
                print(f"{defs.C_RED}  >>> Ch {ch}: ERROR: Less than min ({mon_lvl_v} < {min_val}){defs.C_NONE}")
            elif mon_lvl_v > (max_val + pos_tolerance):
                print(f"{defs.C_RED}  >>> Ch {ch}: ERROR: More than max ({mon_lvl_v} > {max_val}){defs.C_NONE}")
            else:
                print(f"{defs.C_GREEN}  >>> Ch {ch}: OK: {mon_lvl_v} is within range [{min_val}, {max_val}]{defs.C_NONE}")

        int_stat1 = self.ssh_client.gpio_read_AVIVA("PK_08")                            # Read int (pk_07 GPIO) state before test
    
        self.ssh_client.i2c_set(bus, dev, self.REG_UV_HF[ch], f"0x{ov_hf:02x}")         # Set UV_HF to value of OV to trigger UV interrupt
        int_stat2 = self.ssh_client.gpio_read_AVIVA("PK_08")                            # Read int (pk_07 GPIO) state during test
    
        self.ssh_client.i2c_set(bus, dev, self.REG_UV_HF[ch], f"0x{uv_hf:02x}")         # Restore original UV_HF value
        int_stat3 = self.ssh_client.gpio_read_AVIVA("PK_08")                            # Read int (pk_07 GPIO)

        self.print_interrupt_result(f"Ch {ch}: UV", int_stat1, int_stat2, int_stat3)    # Print results of UV interrupt test

        int_stat1 = self.ssh_client.gpio_read_AVIVA("PK_08")                            # Read int (pk_07 GPIO) state before test
    
        self.ssh_client.i2c_set(bus, dev, self.REG_OV_HF[ch], f"0x{uv_hf:02x}")         # Set OV_HF to value of UV to trigger OV interrupt
        int_stat2 = self.ssh_client.gpio_read_AVIVA("PK_08")                            # Read int (pk_07 GPIO) state during test
    
        self.ssh_client.i2c_set(bus, dev, self.REG_OV_HF[ch], f"0x{ov_hf:02x}")         # Restore original OV_HF value
        int_stat3 = self.ssh_client.gpio_read_AVIVA("PK_08")                            # Read int (pk_07 GPIO) state after test    

        self.print_interrupt_result(f"Ch {ch}: OV", int_stat1, int_stat2, int_stat3)    # Print results of OV interrupt test

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Check Device Method to test the functionality of a
    # voltage monitor device by checking each channel
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_device(self, chip: VoltageMonitorChip) -> None:
        bus = chip.bus
        dev = chip.dev

        self.ssh_client.i2c_set(bus, dev, self.REG_BANK_SEL, "0x01")
        vrange_mult = self.ssh_client.i2c_get_int(bus, dev, self.REG_VRANGE_MULT)

        print(defs.C_YELLOW_B)
        print("****************************************************")
        print(f"* Testing {chip.name}: Addr {dev} on i2c bus {bus} *")
        if self.debug_mode:
            ien_uvhf = self.ssh_client.i2c_get(bus, dev, self.REG_IEN_UVHF)
            ien_uvlf = self.ssh_client.i2c_get(bus, dev, self.REG_IEN_UVLF)
            ien_ovhf = self.ssh_client.i2c_get(bus, dev, self.REG_IEN_OVHF)
            ien_ovlf = self.ssh_client.i2c_get(bus, dev, self.REG_IEN_OVLF)
            mon_ch_en = self.ssh_client.i2c_get(bus, dev, self.REG_MON_CH_EN)
            print(
                f"* Int enable: UVHF={ien_uvhf}, UVLF={ien_uvlf}, OVHF={ien_ovhf}, OVLF={ien_ovlf}, MON_CH_EN={mon_ch_en} *"
            )
        print(f"****************************************************{defs.C_NONE}")

        ch_ind = 0
        for ch_info in chip.channels:
            if not ch_info or not ch_info.name:
                continue

            if vrange_mult & (1 << ch_ind):
                self.check_channel(bus, dev, ch_ind, ch_info, 0.8, 0.020)
            else:
                self.check_channel(bus, dev, ch_ind, ch_info, 0.2, 0.005)

            ch_ind += 1

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Run Method to execute the voltage monitor tests for all chips
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main(argv: List[str]) -> int:
    Appl = defs.CApplication(sys.argv)
    rem_client = Appl.create_remote_client()
    rem_client.connect()
    VoltageMonitorTester(rem_client, Appl.debug_mode).run()
    rem_client.close()
    return 0


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
if __name__ == "__main__":
    raise SystemExit(main(sys.argv))