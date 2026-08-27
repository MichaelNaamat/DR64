#!/usr/bin/env python3

import json
import sys
import urllib.request


def read_gpio(pin):
    payload = json.dumps({"log_level": "INFO", "gpios": [pin]}).encode("utf-8")
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
        data = decoded.get("data", [])
        if data:
            val = data[0].get("Val")
            if val is not None:
                return str(val)
    except Exception:
        pass

    return body.strip()


def main():
    pin = sys.argv[1] if len(sys.argv) > 1 else "PK_08"
    state = read_gpio(pin)
    print(f"{pin} {state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
