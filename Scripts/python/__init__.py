import sys
import script_defs as defs

import clock_gen_test
import eeprom_test
import gpio_exp_test
import PMIC_test
import power_supply_test
import temp_sens_int_test
import voltage_mon_test

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main Entry Point
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main() -> int:
    Appl = defs.CApplication(sys.argv)          # Read command line arguments and initialize application
    rem_client = Appl.create_remote_client()    # Create a remote client for communication with the target device
    rem_client.connect()                        # Establish connection with the target device
    
    # --->>> Run tests for various components on the target device
    clock_gen_test.ClockGenTester(rem_client).run()
    eeprom_test.EEPromTester(rem_client).run()
    gpio_exp_test.GPIOExpanderTester(rem_client).run()
    PMIC_test.PMICTester(rem_client).run()
    power_supply_test.PowerSupplyTester(rem_client).run()
    temp_sens_int_test.TempSensorInterruptTester(rem_client).run()
    voltage_mon_test.VoltageMonitorTester(rem_client, Appl.debug_mode).run()
    
    rem_client.close()                          # Close the connection with the target device   
    return 0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Entry point
if __name__ == "__main__":
    raise SystemExit(main())
