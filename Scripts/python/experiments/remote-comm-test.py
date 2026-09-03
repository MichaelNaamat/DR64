import importlib

try:
    paramiko = importlib.import_module("paramiko")
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "The 'paramiko' package is not installed in this Python environment. "
        "Install it with: python -m pip install paramiko"
    ) from e


class run_remote_command:
    def __init__(self, hostname, username, password, command, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.command = command
        self.port = port
        self.ssh_client = None

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {self.hostname}...")
        self.ssh_client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
        )

    def execute(self):
        if self.ssh_client is None:
            raise RuntimeError("SSH connection is not established.")

        print(f"Running command: {self.command}")
        stdin, stdout, stderr = self.ssh_client.exec_command(self.command)
        _ = stdin

        output = stdout.read().decode("utf-8", errors="replace")
        errors = stderr.read().decode("utf-8", errors="replace")

        if output:
            print("\n--- Command Output ---")
            print(output)

        if errors:
            print("\n--- Errors ---")
            print(errors)

        return {"output": output, "errors": errors}

    def close(self):
        if self.ssh_client is not None:
            self.ssh_client.close()
            print("Connection closed.")
            self.ssh_client = None

    def run(self):
        try:
            self.connect()
            return self.execute()
        except Exception as exc:
            print(f"An error occurred: {exc}")
            return {"output": "", "errors": str(exc)}
        finally:
            self.close()


# --- Configuration ---
HOST = "10.0.0.102"      # Replace with your remote Linux IP or hostname
USER = "root"      # Replace with your remote Linux username
PASSWORD = ""  # Replace with your remote Linux password
CMD = "ls -l"  # The command you want to run

# Execute the class instance
run_remote_command(HOST, USER, PASSWORD, CMD).run()