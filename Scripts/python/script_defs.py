## import subprocess
import time
from tokenize import Name
import paramiko
import re
import json
import urllib.request
import serial

# =-=-=-=-=-=-=-=-=<< Constants >>-=-=-=-=-=-=-=-=-=-=-=-
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

SERIAL_COM = "COM3"         # Replace with your serial COM port
SERIAL_BAUD = 115200        # Replace with your serial baud rate
SERIAL_PROMPT = ">"         # Replace with your serial prompt

# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
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

# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# General Client Definition
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CBaseClient:
    def __init__(self, simulate: bool = False):
        self.simulate = simulate

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Pure virtual method for base class, to be implemented by derived classes
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def exec_cmd(self, cmd: str) -> str:
        return "unknown"
    
    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # I2C Get Method to read byte/word register from the device via I2C bus
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def i2c_get(self, bus: str, dev: str, reg: str, mode: str | None = None) -> str:
        cmd = "i2cget -y -f " + bus + " " + dev + " " + reg
        if mode is not None:
            cmd += " " + mode
        if self.simulate:
            return "0x00"

        return self.exec_cmd(cmd)

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # I2C Get Method to read byte/word register from the device via I2C bus, as integer
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def i2c_get_int(self, bus: str, dev: str, reg: str, mode: str | None = None) -> int:
        return int(self.i2c_get(bus, dev, reg, mode), 16)

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # I2C Set Method to write byte/word register to the device via I2C bus
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def i2c_set(self, bus: str, dev: str, reg: str, value: str, mode: str | None = None) -> None:
        cmd = "i2cset -y -f " + bus + " " + dev + " " + reg + " " + value
        if mode is not None:
            cmd += " " + mode
        if self.simulate:
            return
        self.exec_cmd(cmd)

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Method that return the state of GPIO pin (high/low) 
    # by reading the /sys/kernel/debug/gpio file on the 
    # remote Linux host
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def gpio_read(self, pin_name: str) -> str:
        if self.simulate:
            return "unknown"

        cmd = f"cat /sys/kernel/debug/gpio | grep {pin_name}"
        output = self.exec_cmd(cmd)

        match = re.search(r"\b(?:hi|lo)\b", output)
        if match:
            return match.group(0)
        return "unknown"
 
# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# SerialClient Definition
# Parameters:
#   Com: COM port for the serial connection
#   Baud: Baud rate for the serial connection
#   Prompt: Serial prompt for command responses
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CSerialClient(CBaseClient):
    def __init__(self, com: str, baud: int = SERIAL_BAUD, prompt: str = SERIAL_PROMPT, simulate: bool = False):
        super().__init__(simulate=simulate)
        self.com = com
        self.baud = baud
        self.prompt = prompt
        self.serial_port = None

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Connect to the serial port
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def connect(self):
        if self.simulate:
            return
        if self.serial_port is None:        # Protect from opening the serial port multiple times
            self.serial_port = serial.Serial(port=self.com, baudrate=self.baud, timeout=1)
            if not self.serial_port.is_open:
                self.serial_port.open()


    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Close the serial port connection
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def close(self):
        if self.simulate:
            return
        if self.serial_port is not None:
            self.serial_port.close()
            print("Serial connection closed.")
            self.serial_port = None

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Send Command Method to send a command over the serial 
    # connection and read the response
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def exec_cmd(self, cmd: str) -> str:
        if self.simulate:
            return "unknown"

        if self.serial_port is None:
            raise RuntimeError("Serial port is not connected")
    
        self.serial_port.write((cmd + "\n").encode("utf-8"))
        self.serial_port.flush()
        time.sleep(0.1)
    
        output = ""
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self.serial_port.in_waiting:
                chunk = self.serial_port.read(self.serial_port.in_waiting)
                output += chunk.decode("utf-8", errors="replace")
                if self.prompt in output:
                    break
            time.sleep(0.05)
    
        lines = output.splitlines()
        for line in reversed(lines):
            if line.strip() and line.strip() != self.prompt:
                return line.strip()
        return output.strip()
            
# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# SSH Client Definition
# Parameters:
#   hostname: SSH hostname or IP address of the remote Linux host
#   username: SSH username for the remote Linux host
#   password: SSH password for the remote Linux host
#   port: SSH port for the remote Linux host    
#   simulate: Flag to indicate simulation (not accessing H/W, for debugging purposes)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CSSHClient(CBaseClient):
    def __init__(self, hostname, username, password, port=22, simulate: bool = False):
        super().__init__(simulate=simulate)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.ssh_client = None

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Connect to the remote Linux host via SSH
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
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

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Close the SSH connection to the remote Linux host
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def close(self):
        if self.simulate:
            return 
        if self.ssh_client is not None:
            self.ssh_client.close()
            print("Connection closed.")
            self.ssh_client = None
      
    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Execute a command on the remote Linux host via SSH   
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def exec_cmd(self, cmd: str) -> str:
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        output = stdout.read().decode("utf-8", errors="replace")
        errors = stderr.read().decode("utf-8", errors="replace")
        if errors:
            print(f"Errors occurred: {errors}")
        return output.strip()
    
    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def gpio_read_AVIVA (self, pin_name : str) -> str:
        if self.simulate:
            return "unknown"

        GPIO_URL = "http://10.0.0.102:8000/controller/gpio/read_values/"
        payload = json.dumps({"log_level": "INFO", "gpios": [pin_name]}).encode("utf-8")
        request = urllib.request.Request(
            GPIO_URL,
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

        # Convert string "0"/"1" to "lo"/"hi"
        if body.strip() == "0":
            return "lo" 
        elif body.strip() == "1":
            return "hi"
        else:
            return "unknown"
        
# =-=-=-=-=-=-=-=-=<< Object >>-=-=-=-=-=-=-=-=-=-=-=-
# Application object
# Parameters:
#  argv: Command-line arguments
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class CApplication:
    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Constructor
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def __init__(self, argv: list[str]):
        self.argv = argv
        self.link = "ssh"  # Default link type is SSH, can be overridden by command-line argument        
        self.debug_mode = False
        self.sim_mode = False
        
        # --->>> Default values for SSH connection
        self.hostname = SSH_HOST
        self.username = SSH_USER
        self.password = SSH_PASSWORD
        
        # --->>> Default values for Serial connection
        self.com    = SERIAL_COM
        self.baud   = SERIAL_BAUD
        self.prompt = SERIAL_PROMPT

        self.read_args()  # Read command-line arguments to override defaults

    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # Read command-line arguments to override default values
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def read_args(self):
        for arg in self.argv[1:]:
            if arg == "-debug":
                self.debug_mode = True
            if arg == "-sim":
                self.sim_mode = True
            elif arg.startswith("-link="):
                self.link = arg.split("=")[1]
            # --->>> SSH connection parameters    
            elif arg.startswith("-host="):
                self.hostname = arg.split("=")[1]
            elif arg.startswith("-user="):
                self.username = arg.split("=")[1]                
            elif arg.startswith("-pw="):
                 self.password = arg.split("=")[1] 
            # --->>> Serial connection parameters
            elif arg.startswith("-baud="):
                 self.baud = int(arg.split("=")[1])
            elif arg.startswith("-com="):
                 self.com = arg.split("=")[1]  
            elif arg.startswith("-prompt="):
                 self.prompt = arg.split("=")[1]
                 
    # =-=-=-=-=-=-=-=-=<< Method >>-=-=-=-=-=-=-=-=-=-=-=-
    # llocate client-link object according to command-line 
    # argument and connect to the remote host
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def create_remote_client(self) -> CBaseClient:
        match self.link:
            case "ssh":
                client = CSSHClient(hostname=self.hostname, username=self.username, password=self.password, simulate=self.sim_mode)
            case "serial":
                client = CSerialClient(com=self.com, baud=self.baud, prompt=self.prompt, simulate=self.sim_mode)
            case _:
                print(f"{C_RED_B}  >>> ERROR: Unsupported link type '{self.link}' specified!{C_NONE}")
                raise ValueError(f"Unsupported link type '{self.link}' specified!")
        return client