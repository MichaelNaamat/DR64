#!/usr/bin/env python3

import json
import os
import re
import time
import urllib.request

import serial


def normalize_serial_port(port: str) -> str:
    """Normalize a serial port name across Linux and Windows environments."""
    if not port:
        return port

    port = port.strip()
    if os.name == "nt":
        if port.upper().startswith("COM"):
            return port

        match = re.search(r"(ttyS|ttyUSB|ttyACM)(\d+)", port)
        if match:
            return f"COM{int(match.group(2))}"

        if port.startswith("/dev/"):
            match = re.search(r"(\d+)$", port)
            if match:
                return f"COM{int(match.group(1))}"

    return port


class CSerialClient:
    """Serial-port client that mirrors the CSSHClient interface for remote commands.

    This class provides the same high-level methods as the SSH version but routes
    execution through a serial console / serial shell instead of an SSH session.
    """

    def __init__(
        self,
        port: str = "COM3",
        baudrate: int = 115200,
        timeout: float = 1.0,
        simulate: bool = False,
        prompt: str = ">",
    ):
        self.port = normalize_serial_port(port)
        self.baudrate = baudrate
        self.timeout = timeout
        self.simulate = simulate
        self.prompt = prompt
        self.serial_port = None

    def connect(self) -> None:
        if self.simulate:
            return

        self.serial_port = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            write_timeout=self.timeout,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        )
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        self._wait_for_prompt()

    def close(self) -> None:
        if self.serial_port is not None:
            self.serial_port.close()
            self.serial_port = None

    def _wait_for_prompt(self, timeout: float = 5.0) -> str:
        if self.simulate or self.serial_port is None:
            return ""

        deadline = time.monotonic() + timeout
        buffer = ""
        while time.monotonic() < deadline:
            if self.serial_port.in_waiting:
                chunk = self.serial_port.read(self.serial_port.in_waiting)
                if chunk:
                    buffer += chunk.decode("utf-8", errors="replace")
                    if self.prompt in buffer:
                        break
            time.sleep(0.05)
        return buffer

    def _send_command(self, cmd: str) -> str:
        if self.simulate:
            return "0x00"

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

    def i2c_get(self, bus: str, dev: str, reg: str, mode: str | None = None) -> str:
        cmd = f"i2cget -y -f {bus} {dev} {reg}"
        if mode is not None:
            cmd += f" {mode}"

        if self.simulate:
            return "0x00"

        return self._send_command(cmd)

    def i2c_get_int(self, bus: str, dev: str, reg: str, mode: str | None = None) -> int:
        return int(self.i2c_get(bus, dev, reg, mode), 16)

    def i2c_set(self, bus: str, dev: str, reg: str, value: str, mode: str | None = None) -> None:
        cmd = f"i2cset -y -f {bus} {dev} {reg} {value}"
        if mode is not None:
            cmd += f" {mode}"

        if self.simulate:
            return

        self._send_command(cmd)

    def gpio_read(self, pin_name: str) -> str:
        if self.simulate:
            return "unknown"

        cmd = f"cat /sys/kernel/debug/gpio | grep {pin_name}"
        output = self._send_command(cmd)
        match = re.search(r"\b(?:hi|lo)\b", output, re.IGNORECASE)
        if match:
            return match.group(0).lower()
        return "unknown"

    def gpio_read_AVIVA(self, pin_name: str) -> str:
        if self.simulate:
            return "unknown"

        try:
            payload = json.dumps({"log_level": "INFO", "gpios": [pin_name]}).encode("utf-8")
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

            if body.strip() == "0":
                return "lo"
            if body.strip() == "1":
                return "hi"
            return "unknown"
        except Exception:
            return self.gpio_read(pin_name)
