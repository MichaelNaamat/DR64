#!/bin/bash

source ./script_defs.sh     # Include general definitions for all tests (colors, etc.)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Get value (0/1) of a GPIO pin
# Parameters:
# $1 - GPIO pin identifier
# Return: 0 or 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function vmon_get_pin()
{
    local cmd_out pin_state

##    cmd_out=$(wget -qO- --method=POST \
##                   --header='accept: application/json' \
##                   --header='Content-Type: application/json' \
##                   --body-data='{"log_level": "INFO", "gpios": ["'"$1"'"]}' \
##                   "http://10.0.0.102:8000/controller/gpio/read_values/")
##
##    pin_state=${cmd_out:129:1}
    pin_state="0"
    echo -e "$pin_state"
}

int_stat1=$(vmon_get_pin "PK_08")

#    i2cset -y -f $bus $dev ${REG_UV_HF[$ch]} $ov_hf             # Set UV_HF to value of OV to trigger UV interrupt
    int_stat2=$(vmon_get_pin "PK_08")     # Read int (pk_07 GPIO) state during test

#    i2cset -y -f $bus $dev ${REG_UV_HF[$ch]} $uv_hf             # Restore original UV_HF value
    int_stat3=$(vmon_get_pin "PK_08")     # Read int (pk_07 GPIO)

    echo -n "  >>> Ch 0: UV interrupt state: Before(${int_stat1}), During(${int_stat2}), After(${int_stat3}): "
    test "$int_stat1" = "0" && echo -e -n "${C_RED_B}FAIL,${C_NONE}" || echo -e -n "${C_GREEN_B}Pass,${C_NONE}"
    test "$int_stat2" = "1" && echo -e -n "${C_RED_B}FAIL,${C_NONE}" || echo -e -n "${C_GREEN_B}Pass,${C_NONE}"
    test "$int_stat3" = "0" && echo -e -n "${C_RED_B}FAIL${C_NONE}"  || echo -e -n "${C_GREEN_B}Pass${C_NONE}"
    echo
