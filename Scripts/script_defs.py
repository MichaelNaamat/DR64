## import subprocess
from tokenize import Name
import paramiko
import re
import json
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
# SSH Client Definition
# Parameters:
#   simulate: Flag to indicate simulation (not accessing H/W, for debugging purposes)
#   dev: I2C device address as a string (e.g., "0x37")
#   reg: Register address as a string (e.g., "0x01")
#   mode: Optional mode for I2C access (e.g., "b" for byte, "w" for word)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CSSHClient:
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
    def i2c_get(self, bus: str, dev: str, reg: str, mode: str | None = None) -> str:
        cmd = "i2cget -y -f " + bus + " " + dev + " " + reg
        if mode is not None:
            cmd += " " + mode

        if self.simulate:
            return "0x00"

        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        _ = stdin

        output = stdout.read().decode("utf-8", errors="replace")
        errors = stderr.read().decode("utf-8", errors="replace")
        if errors:
            print(f"Errors occurred: {errors}")
        return output.strip()
    
    # --->>> I2C Get Method to read byte/word register from the device via I2C bus, as integer
    def i2c_get_int(self, bus: str, dev: str, reg: str, mode: str | None = None) -> int:
        return int(self.i2c_get(bus, dev, reg, mode), 16)

    # --->>> I2C Set Method to write byte/word register to the device via I2C bus
    def i2c_set(self, bus: str, dev: str, reg: str, value: str, mode: str | None = None) -> None:
        if self.simulate:
            return

        cmd = "i2cset -y -f " + bus + " " + dev + " " + reg + " " + value
        if mode is not None:
            cmd += " " + mode

        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        _ = stdin

        output = stdout.read().decode("utf-8", errors="replace")
        errors = stderr.read().decode("utf-8", errors="replace")
        if errors:
            print(f"Errors occurred: {errors}")

    # --->>> Method that return the state of GPIO pin (high/low) by reading the /sys/kernel/debug/gpio file on the remote Linux host
    def gpio_read(self, pin_name: str) -> str:
        if self.simulate:
            return "unknown"

        cmd = f"cat /sys/kernel/debug/gpio | grep {pin_name}"
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        _ = stdin

        output = stdout.read().decode("utf-8", errors="replace")
        errors = stderr.read().decode("utf-8", errors="replace")
        if errors:
            print(f"Errors occurred: {errors}")

        match = re.search(r"\b(?:hi|lo)\b", output)
        if match:
            return match.group(0)
        return "unknown"
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def gpio_read_AVIVA (self, pin_name : str) -> str:
        if self.simulate:
            return "unknown"

        GPIO_URL = "http://10.0.0.102:8000/controller/gpio/read_values/"
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

