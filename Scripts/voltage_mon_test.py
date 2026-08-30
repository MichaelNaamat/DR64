#!/usr/bin/env python3

import json
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from typing import List, Optional

import script_defs as defs

@dataclass(frozen=True)
class VoltageChannel:
    name: str
    min_val: float
    typ_val: float
    max_val: float


@dataclass(frozen=True)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Voltage Monitor Chip Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class VoltageMonitorChip:
    name: str
    bus: str
    dev: str
    channels: List[Optional[VoltageChannel]]


def channel(name: str, min_val: float, typ_val: float, max_val: float) -> VoltageChannel:
    return VoltageChannel(name=name, min_val=min_val, typ_val=typ_val, max_val=max_val)

class VoltageMonitorClient:
    GPIO_URL = "http://10.0.0.102:8000/controller/gpio/read_values/"

    def __init__(self, simulate: bool = False):
        self.simulate = simulate

## DEAD    def run_command(self, args: List[str]) -> str:
## DEAD        if self.simulate:
## DEAD            return "0xAA"
## DEAD        completed = subprocess.run(args, capture_output=True, text=True, check=True)
## DEAD        return completed.stdout.strip()
## DEAD
## DEAD    def i2cget(self, bus: str, dev: str, reg: str) -> str:
## DEAD        return self.run_command(["i2cget", "-y", "-f", bus, dev, reg])
## DEAD
## DEAD    def i2cset(self, bus: str, dev: str, reg: str, value: str) -> None:
## DEAD        self.run_command(["i2cset", "-y", "-f", bus, dev, reg, value])

    def vmon_get_pin(self, pin: str) -> str:
        if self.simulate:
            return "0"

        payload = json.dumps({"log_level": "INFO", "gpios": [pin]}).encode("utf-8")
        request = urllib.request.Request(
            self.GPIO_URL,
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

    def read_hex_int(self, bus: str, dev: str, reg: str) -> int:
        return int(self.i2cget(bus, dev, reg), 0)

    @staticmethod
    def format_voltage(raw_value: int, coef: float, mul: float) -> str:
        return f"{coef + raw_value * mul:.3f}"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
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

    def __init__(self, chips: List[VoltageMonitorChip], i2c_client: defs.I2CClient, client: VoltageMonitorClient, debug_mode: bool):
        self.chips = chips
        self.i2c_client = i2c_client
        self.client = client
        self.debug_mode = debug_mode

    @staticmethod
    def print_interrupt_result(label: str, before_state: str, during_state: str, after_state: str) -> None:
        print(
            f"  >>> {label} interrupt state: Before({before_state}), During({during_state}), After({after_state}): ",
            end="",
        )
        print(
            f"{defs.C_RED_B}FAIL,{defs.C_NONE}" if before_state == "0" else f"{defs.C_GREEN_B}Pass,{defs.C_NONE}",
            end="",
        )
        print(
            f"{defs.C_RED_B}FAIL,{defs.C_NONE}" if during_state == "1" else f"{defs.C_GREEN_B}Pass,{defs.C_NONE}",
            end="",
        )
        print(
            f"{defs.C_RED_B}FAIL{defs.C_NONE}" if after_state == "0" else f"{defs.C_GREEN_B}Pass{defs.C_NONE}"
        )

    def check_channel(self, bus: str, dev: str, ch: int, ch_info: VoltageChannel, coef: float, mul: float) -> None:
        min_val = ch_info.min_val
        typ_val = ch_info.typ_val
        max_val = ch_info.max_val

        self.i2c_client.set(bus, dev, self.REG_BANK_SEL, "0x00")
        mon_lvl = self.i2c_client.get(bus, dev, self.REG_VMON_LVL[ch])

        self.i2c_client.set(bus, dev, self.REG_BANK_SEL, "0x01")
        uv_hf = self.i2c_client.get(bus, dev, self.REG_UV_HF[ch])
        ov_hf = self.i2c_client.get(bus, dev, self.REG_OV_HF[ch])
        uv_lf = self.i2c_client.get(bus, dev, self.REG_UV_LF[ch])
        ov_lf = self.i2c_client.get(bus, dev, self.REG_OV_LF[ch])

        if mon_lvl <= 0 or mon_lvl > 255:
            print(f"{defs.C_RED_B}  >>> ERROR: Invalid monitor level ({mon_lvl}) for channel {ch}{defs.C_NONE}")
            return

        if self.debug_mode:
            mon_lvl_v = self.i2c_client.format_voltage(mon_lvl, coef, mul)
            uv_hf_v = self.i2c_client.format_voltage(uv_hf, coef, mul)
            ov_hf_v = self.i2c_client.format_voltage(ov_hf, coef, mul)
            uv_lf_v = self.i2c_client.format_voltage(uv_lf, coef, mul)
            ov_lf_v = self.i2c_client.format_voltage(ov_lf, coef, mul)

            print(
                f"{defs.C_BLUE_B}  >>> DEBUG: Ch {ch}: min={min_val}, typ={typ_val}, max={max_val}, MON_LVL={mon_lvl_v}({mon_lvl})"
            )
            print(
                f"                             UV_HF={uv_hf_v}({uv_hf}) OV_HF={ov_hf_v}({ov_hf}) UV_LF={uv_lf_v}({uv_lf}) OV_LF={ov_lf_v}({ov_lf}){defs.C_NONE}"
            )

            if float(mon_lvl_v) < min_val:
                print(f"{defs.C_RED}  >>> Ch {ch}: ERROR: Less than min ({mon_lvl_v} < {min_val}){defs.C_NONE}")
            elif float(mon_lvl_v) > max_val:
                print(f"{defs.C_RED}  >>> Ch {ch}: ERROR: More than max ({mon_lvl_v} > {max_val}){defs.C_NONE}")
            else:
                print(f"{defs.C_GREEN}  >>> Ch {ch}: OK: {mon_lvl_v} is within range [{min_val}, {max_val}]{defs.C_NONE}")

        int_stat1 = self.i2c_client.read("PK_08")

        self.i2c_client.set(bus, dev, self.REG_UV_HF[ch], f"0x{ov_hf:02x}")
        int_stat2 = self.i2c_client.read("PK_08")

        self.i2c_client.set(bus, dev, self.REG_UV_HF[ch], f"0x{uv_hf:02x}")
        int_stat3 = self.i2c_client.read("PK_08")

        self.print_interrupt_result(f"Ch {ch}: UV", int_stat1, int_stat2, int_stat3)

        int_stat1 = self.i2c_client.read("PK_08")

        self.i2c_client.set(bus, dev, self.REG_OV_HF[ch], f"0x{uv_hf:02x}")
        int_stat2 = self.i2c_client.read("PK_08")

        self.i2c_client.set(bus, dev, self.REG_OV_HF[ch], f"0x{ov_hf:02x}")
        int_stat3 = self.i2c_client.read("PK_08")

        self.print_interrupt_result(f"Ch {ch}: OV", int_stat1, int_stat2, int_stat3)

    def check_device(self, chip: VoltageMonitorChip) -> None:
        bus = chip.bus
        dev = chip.dev

        self.i2c_client.set(bus, dev, self.REG_BANK_SEL, "0x01")
        vrange_mult = self.i2c_client.get(bus, dev, self.REG_VRANGE_MULT)

        print(defs.C_YELLOW)
        print("****************************************************")
        print(f"* Testing {chip.name}: Addr {dev} on i2c bus {bus} *")
        if self.debug_mode:
            ien_uvhf = self.i2c_client.get(bus, dev, self.REG_IEN_UVHF)
            ien_uvlf = self.i2c_client.get(bus, dev, self.REG_IEN_UVLF)
            ien_ovhf = self.i2c_client.get(bus, dev, self.REG_IEN_OVHF)
            ien_ovlf = self.i2c_client.get(bus, dev, self.REG_IEN_OVLF)
            mon_ch_en = self.i2c_client.get(bus, dev, self.REG_MON_CH_EN)
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

    def run(self) -> None:
        for chip in self.chips:
            self.check_device(chip)


class VoltageMonitorApplication:
    def __init__(self, argv: List[str]):
        self.argv = argv
        self.chips = self._build_chips()

    @staticmethod
    def _build_chips() -> List[VoltageMonitorChip]:
        u93_channels: List[Optional[VoltageChannel]] = [
            channel("0.875V (core) +2.5% / -3%", 0.84875, 0.875, 0.896875),
            channel("1.8V (PCIE) +/-5%", 1.71, 1.8, 1.89),
            channel("1.8V (IP) +/-3%", 1.746, 1.8, 1.854),
            channel("0.86V (PCIE) +/-5%", 0.817, 0.86, 0.903),
            channel("0.75V (MIPI) +/-5%", 0.7125, 0.75, 0.7875),
            channel("1.05V (DDR) +/-3%", 1.0185, 1.05, 1.0815),
            channel("0.5V (DDR) +/-5%", 0.475, 0.5, 0.525),
            channel("1.8V (Main) +/-5%", 1.71, 1.8, 1.89),
        ]

        u94_channels: List[Optional[VoltageChannel]] = [
            channel("0.875V (core) +2.5% / -3%", 0.84875, 0.875, 0.896875),
            channel("1.8V (PCIE) +/-5%", 1.71, 1.8, 1.89),
            channel("1.8V (IP) +/-3%", 1.746, 1.8, 1.854),
            channel("0.86V (PCIE) +/-5%", 0.817, 0.86, 0.903),
            channel("0.75V (MIPI) +/-5%", 0.7125, 0.75, 0.7875),
            channel("1.05V (DDR) +/-3%", 1.0185, 1.05, 1.0815),
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

        return [
            VoltageMonitorChip(name="U93", bus="0x00", dev="0x37", channels=u93_channels),
            VoltageMonitorChip(name="U94", bus="0x00", dev="0x36", channels=u94_channels),
            VoltageMonitorChip(name="U95", bus="0x00", dev="0x35", channels=u95_channels),
            VoltageMonitorChip(name="U114", bus="0x00", dev="0x34", channels=u114_channels),
        ]

    def configure_modes(self) -> None:
        defs.debug_mode = False
        defs.sim_mode = False

        for arg in self.argv[1:]:
            if arg == "debug":
                defs.debug_mode = True
            elif arg == "sim":
                defs.sim_mode = True

    def run(self) -> int:
        self.configure_modes()
        client = VoltageMonitorClient(simulate=defs.sim_mode)
        VoltageMonitorTester(self.chips, client, defs.debug_mode).run()
        return 0


def main(argv: List[str]) -> int:
    return VoltageMonitorApplication(argv).run()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
if __name__ == "__main__":
    raise SystemExit(main(sys.argv))