#!/usr/bin/env python3
from dataclasses import dataclass
import sys
import time

import script_defs as defs

@dataclass(frozen=False)

# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# Temperature Sensor Interrupt Tester Class Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class TempSensorInterruptTester:
    REG_TEMP = "0x00"
    REG_CR = "0x01"
    REG_TLOW = "0x02"
    REG_THIGH = "0x03"
    REG_OS = "0x04"

    chips = [
        defs.CChipDef(name="U60" , bus="0x04", dev="0x48"),
        defs.CChipDef(name="U61" , bus="0x04", dev="0x4C"),
        defs.CChipDef(name="U62" , bus="0x04", dev="0x49"),
        defs.CChipDef(name="U64" , bus="0x04", dev="0x4A"),
        defs.CChipDef(name="U127", bus="0x00", dev="0x49"),
    ]

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Constructor Method to initialize the TempSensorInterruptTester 
    # class with a list of chip definitions and a remote 
    # client for communication
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, rem_client: defs.CBaseClient):
        self.rem_client = rem_client

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Print Header Method to display a header for the chip 
    # being tested, including T-Low and T-High values
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def _print_header(self, chip: defs.CChipDef, t_low: str, t_high: str) -> None:
        print(f"{defs.C_YELLOW_B}")
        print("****************************************************")
        print(f"* Testing Temp Sens {chip.name}: Addr {chip.dev} on i2c bus {chip.bus}")
        print(f"* T-Low={t_low}c, T-High={t_high}c")
        print("****************************************************")
        print(f"{defs.C_NONE}", end="")

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Check Interrupt Method to verify the functionality of the
    # temperature sensor interrupt by setting T-Low and T-High 
    # values and checking the GPIO state before, during, and after
    # the test
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def check_interrupt(self, chip: defs.CChipDef) -> None:
        org_t_low = self.rem_client.i2c_get(chip.bus, chip.dev, self.REG_TLOW, "w")
        org_t_high = self.rem_client.i2c_get(chip.bus, chip.dev, self.REG_THIGH, "w")

        self._print_header(chip, org_t_low, org_t_high)
        time.sleep(0.1)

        # --->>> Set Configuration Reg (0x01):
        # OS (15)    = '0'
        # CR (13-14) = '00'  | 37Hz conversion rate (typ) (default)
        # FQ (11-12) = '00'  | 1 fault (default)
        # POL (10)   = '0'   | ALERT is active low (default)
        # TM  (9)    = '0'   | ALERT is in comperator mode (default)
        # SD  (8)    = '0'   | Device is in continuous conversion mode (default)
        # Mask: 0000 0000 = 0x00
        self.rem_client.i2c_set(chip.bus, chip.dev, self.REG_CR, "0x00")

        # ============ T-High test: Set T-High to +5c, T-Low to +2
        int_before = self.rem_client.gpio_read("PC_04")     # Read GPIO before setting T-High/T-Low

        self.rem_client.i2c_set(chip.bus, chip.dev, self.REG_THIGH, "+5", "w")  # Set T-High to +5c
        self.rem_client.i2c_set(chip.bus, chip.dev, self.REG_TLOW, "+2", "w")   # Set T-Low to +2c

        int_during = self.rem_client.gpio_read("PC_04")     # Read GPIO after setting T-High/T-Low

        # --->>> Read T-Low/T-High values & clear interrupt
        t_low = self.rem_client.i2c_get(chip.bus, chip.dev, self.REG_TLOW, "w")
        t_high = self.rem_client.i2c_get(chip.bus, chip.dev, self.REG_THIGH, "w")

        # --->>> Restore normal values 
        self.rem_client.i2c_set(chip.bus, chip.dev, self.REG_TLOW, org_t_low, "w")
        self.rem_client.i2c_set(chip.bus, chip.dev, self.REG_THIGH, org_t_high, "w")

        # --->>> Read current temperature
        cur_temp = self.rem_client.i2c_get_int(chip.bus, chip.dev, self.REG_TEMP, "w")
        cur_temp = (cur_temp & 0xFF ) + (((cur_temp >> 8) & 0xFF) * 0.0625)

        int_after = self.rem_client.gpio_read("PC_04")      # Read GPIO after restoring T-High/T-Low values

        # ---->>> Print results of interrupt test
        print(
            f"  T-High/T-Low test: Temp={cur_temp}c, T-Low={t_low}c, T-High={t_high}c, "
            f"Before({int_before}), During({int_during}), After({int_after}) - ",
            end="",
        )

        if int_before == "hi":
            print(f"{defs.C_GREEN_B}Pass,{defs.C_NONE}", end="")
        else:
            print(f"{defs.C_RED_B}FAIL,{defs.C_NONE}", end="")

        if int_during == "lo":
            print(f"{defs.C_GREEN_B}Pass,{defs.C_NONE}", end="")
        else:
            print(f"{defs.C_RED_B}FAIL,{defs.C_NONE}", end="")

        if int_after == "hi":
            print(f"{defs.C_GREEN_B}Pass{defs.C_NONE}")
        else:
            print(f"{defs.C_RED_B}FAIL{defs.C_NONE}")
    
    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Run Method to iterate through the list of chips and 
    # check each interrupt
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def run(self) -> None:
        for chip in self.chips:
            self.check_interrupt(chip)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main():
    Appl = defs.CApplication(sys.argv)
    rem_client = Appl.create_remote_client()
    rem_client.connect()
    TempSensorInterruptTester(rem_client).run()
    rem_client.close()
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
