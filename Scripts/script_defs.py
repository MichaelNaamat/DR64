import subprocess
from tokenize import Name
import paramiko
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

SSH_HOST = "10.0.0.102"     # Replace with your remote Linux IP or hostname
SSH_USER = "root"           # Replace with your remote Linux username
SSH_PASSWORD = ""           # Replace with your remote Linux password

global debug_mode, sim_mode

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Chip Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CChipDef:
    name: str
    bus: str
    dev: str
    def __init__(self, name, bus, dev):
        self.name = name
        self.bus = bus
        self.dev = dev

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# I2C Client Definition
# Parameters:
#   simulate: Flag to indicate simulation (not accessing H/W, for debugging purposes)
#   dev: I2C device address as a string (e.g., "0x37")
#   reg: Register address as a string (e.g., "0x01")
#   mode: Optional mode for I2C access (e.g., "b" for byte, "w" for word)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class I2CClient:
    def __init__(self, hostname, username, password, port=22, simulate: bool = False):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.simulate = simulate
        self.ssh_client = None

    # --->>> Connect to the remote Linux host via SSH
    def connect(self):
        if self.simulate:
            return 
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {self.hostname}...")
        self.ssh_client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
        )

    # --->>> Close the SSH connection to the remote Linux host
    def close(self):
        if self.simulate:
            return 
        if self.ssh_client is not None:
            self.ssh_client.close()
            print("Connection closed.")
            self.ssh_client = None

    # --->>> I2C Get Method to read byte/word register from the device via I2C bus
    def get(self, bus: str, dev: str, reg: str, mode: str | None = None) -> str:
        cmd = "i2cget -y -f " + bus + " " + dev + " " + reg
        if mode is not None:
            cmd += " " + mode

        if self.simulate:
            return "0x00"

##        completed = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
##        return completed.stdout.strip()
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        _ = stdin

        output = stdout.read().decode("utf-8", errors="replace")
        errors = stderr.read().decode("utf-8", errors="replace")
        if errors:
            print(f"Errors occurred: {errors}")
        return output.strip()
    
    # --->>> I2C Get Method to read byte/word register from the device via I2C bus, as integer
    def get_int(self, bus: str, dev: str, reg: str, mode: str | None = None) -> int:
        return int(self.get(bus, dev, reg, mode), 16)
    
    # --->>> I2C Set Method to write byte/word register to the device via I2C bus
    def set(self, bus: str, dev: str, reg: str, value: str, mode: str | None = None) -> None:
        if self.simulate:
            return

        cmd = "i2cset -y -f " + bus + " " + dev + " " + reg + " " + value
        if mode is not None:
            cmd += " " + mode

        subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
        
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

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Get program modes according to command-line arguments
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def configure_modes(argv: list[str]) :
    global debug_mode, sim_mode
    debug_mode = False
    sim_mode = False
    for arg in argv[1:]:
        if arg == "debug":
            debug_mode = True
        elif arg == "sim":
            sim_mode = True

