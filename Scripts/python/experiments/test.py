#!/usr/bin/env python3

import json
import sys
import urllib.request

C_RED_B = "\033[1;31m"
C_GREEN_B = "\033[1;32m"
C_NONE = "\033[0m"


def vmon_get_pin(pin):
    payload = json.dumps({"log_level": "INFO", "gpios": [pin]}).encode("utf-8")
    request = urllib.request.Request(
        "http://10.0.0.102:8000/controller/gpio/read_values/",
        data=payload,
        headers={"accept": "application/json", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
    except Exception:
        return "0"

    try:
        decoded = json.loads(body)
        data = decoded.get("data", [])
        if data:
            val = data[0].get("Val")
            if val is not None:
                return str(val)
    except Exception:
        pass
    return "0"


def main():
    int_stat1 = vmon_get_pin("PK_08")
    int_stat2 = vmon_get_pin("PK_08")
    int_stat3 = vmon_get_pin("PK_08")

    print(f"  >>> Ch 0: UV interrupt state: Before({int_stat1}), During({int_stat2}), After({int_stat3}): ", end="")
    if int_stat1 == "0":
        print(f"{C_RED_B}FAIL,{C_NONE}", end="")
    else:
        print(f"{C_GREEN_B}Pass,{C_NONE}", end="")

    if int_stat2 == "1":
        print(f"{C_RED_B}FAIL,{C_NONE}", end="")
    else:
        print(f"{C_GREEN_B}Pass,{C_NONE}", end="")

    if int_stat3 == "0":
        print(f"{C_RED_B}FAIL{C_NONE}")
    else:
        print(f"{C_GREEN_B}Pass{C_NONE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
