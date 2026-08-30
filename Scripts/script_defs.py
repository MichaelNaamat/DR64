import subprocess
import re

C_RED = "\033[0;31m"
C_GREEN = "\033[0;32m"
C_YELLOW = "\033[0;33m"
C_BLUE = "\033[0;34m"
C_RED_B = "\033[1;31m"
C_GREEN_B = "\033[1;32m"
C_YELLOW_B = "\033[1;33m"
C_BLUE_B = "\033[1;34m"
C_NONE = "\033[0m"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Chip Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CChipDef:
    name: str
    bus: str
    dev: str

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# I2C Client Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class I2CClient:
    def __init__(self, simulate: bool = False):
        self.simulate = simulate

    # --->>> I2C Get Method to read byte/word register from the device via I2C bus
    def get(self, bus: str, dev: str, reg: str, mode: str | None = None) -> str:
        if self.simulate:
            return "0x00"

        args = ["i2cget", "-y", "-f", bus, dev, reg]
        if mode is not None:
            args.append(mode)

        completed = subprocess.run(args, capture_output=True, text=True, check=True)
        return completed.stdout.strip()
    
    # --->>> I2C Get Method to read byte/word register from the device via I2C bus, as integer
    def get_int(self, bus: str, dev: str, reg: str, mode: str | None = None) -> int:
        return int(self.get(bus, dev, reg, mode), 16)
    
    # --->>> I2C Set Method to write byte/word register to the device via I2C bus
    def set(self, bus: str, dev: str, reg: str, value: str, mode: str | None = None) -> None:
        if self.simulate:
            return

        args = ["i2cset", "-y", "-f", bus, dev, reg, value]
        if mode is not None:
            args.append(mode)

        subprocess.run(args, capture_output=True, text=True, check=True)
        
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# GPIO Reader Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CGPIOReader:
    @staticmethod
    def read(PinName: str) -> str:
        try:
            with open("/sys/kernel/debug/gpio", "r", encoding="utf-8") as file:
                lines = file.read().splitlines()
        except OSError:
            return "unknown"

        for line in lines:
            if PinName in line:
                match = re.search(r"\b(?:hi|lo)\b", line)
                if match:
                    return match.group(0)
                return "unknown"

        return "unknown"

