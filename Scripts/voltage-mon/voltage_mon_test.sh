#!/bin/bash

declare -a vmon_bus=("0x00" "0x00" "0x00" "0x00")
declare -a vmon_dev=("0x34" "0x35" "0x36" "0x37")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Print values of voltage monitor registers for a given device
# Parameters:
# $1 - Bus number
# $2 - Device number
# $3 - Monitor channel (0..7)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function read_vmon_channel()
{
    local bus dev ch
    bus=$1
    dev=$2
    ch=$3
}
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Do test on VMON device
# Parameters:
# $1 - Bus number
# $2 - Device number
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function check_vmon_dev()
{
    local bus dev
    bus=$1
    dev=$2

    echo "*****************************************"
    echo "* Testing VMON Dev $dev on i2c bus $bus"
    echo "*****************************************"

    # DEBUG: Read all 8 channels of the device
    for ch in {0..7}
    do
        read_vmon_channel $bus $dev $ch
    done
}

# ---->>>> Call tests for all devices...
for i in {0..3}
do
    check_vmon_dev ${vmon_bus[$i]} ${vmon_dev[$i]}
done
