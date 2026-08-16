#!/bin/bash

declare -a VMON_BUS=("0x00" "0x00" "0x00" "0x00")
declare -a VMON_DEV=("0x34" "0x35" "0x36" "0x37")


# -------------------- Bank independent ------------------------
declare -r REG_BANK_SEL="0xF0"

# -------------------- Bank 0 registers ------------------------
# --->>> Reg addresses of MON_LVL[i] for channels 0..7
declare -a VMON_LVL_REG=("0x40" "0x41" "0x42" "0x43" "0x44" "0x45" "0x46" "0x47")   

# -------------------- Bank 1 registers ------------------------
declare -r REG_VRANGE_MUL="0x1F"   

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Print values of voltage monitor registers for a given device
# Parameters:
# $1 - Bus number
# $2 - Device number
# $3 - Monitor channel (0..7)
# $4 - VRANGE_MULT value (1..4 for 1x..4x)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function check_vmon_channel()
{
    local bus dev ch mon_lvl mul_val volt_val
    bus=$1
    dev=$2
    ch=$3
    vrange_mul=$4

    mon_lvl=$(i2cget -y -f $bus $dev ${VMON_LVL_REG[$ch]})

    case $vrange_mul in
        0) volt_val=$(awk -v a="$mon_lvl"  'BEGIN { printf "%.3f", 0.2 + a * 0.005 }') ;;
        1) volt_val=$(awk -v a="$mon_lvl"  'BEGIN { printf "%.3f", 0.8 + a * 0.02 }') ;;
        *) echo "** Invalid VRANGE_MULT." ; exit 1 ;;
    esac

    echo "VOLT_VAL=$volt_val"  ## DEBUG
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
    local bus dev vrange_mul
    bus=$1
    dev=$2

    echo "*****************************************"
    echo "* Testing VMON Dev $dev on i2c bus $bus"
    echo "*****************************************"

    # --->>> First - read the value of VRANGE_MULT from bank 1, register 0xF1
    i2cset -y -f $bus $dev $REG_BANK_SEL 1   # Move to bank 1
    vrange_mul=$(i2cget -y -f $bus $dev $REG_VRANGE_MUL)
    i2cset -y -f $bus $dev $REG_BANK_SEL 0   # Move back to bank 0
    
    # DEBUG: Read all 8 channels of the device
    for ch in {0..7}
    do
        check_vmon_channel $bus $dev $ch $vrange_mul
    done
}

# ---->>>> Call tests for all devices...
for i in {0..3}
do
    check_vmon_dev ${VMON_BUS[$i]} ${VMON_DEV[$i]}
done
