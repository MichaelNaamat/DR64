#!/bin/bash

pin=$1

int_state=$(wget -qO- --method=POST \
--header='accept: application/json' \
--header='Content-Type: application/json' \
--body-data='{"log_level": "INFO", "gpios": ["'"$1"'"]}' \
"http://10.0.0.102:8000/controller/gpio/read_values/")

## {"timestamp":"2026-05-16T00:07:31.363418","message":null,"logs":[],"data":[{"Name":"PK_08","Net":"SAFETY_SIG.VMs_3v3_INT","Val":"1","Dir":"Input","Edge":"Both","Mon":"ON"}]}
echo $int_state
pin_state=${int_state:129:1}

echo $pin $pin_state
