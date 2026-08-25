#!/bin/bash

source ./script_defs.sh     # Include general definitions for all tests (colors, etc.)

# --->>> Register definition
declare -r REG_PS_VSET="0x00"   # Output Voltage Setpoint
declare -r REG_PS_CONTROL1="0x01"   # Control Register 1
declare -r REG_PS_CONTROL2="0x02"   # Control Register 2
declare -r REG_PS_CONTROL3="0x03"   # Control Register 3
declare -r REG_PS_STATUS="0x04"     # Status Register

# ----->>> Define Power Supply chips
declare -A ps_chip_U33=(    name "U33"    bus "0x01" dev "0x33" )
declare -A ps_chip_A_U26=(  name "A_U26"  bus "0x01" dev "0x40" )
declare -A ps_chip_A_U18=(  name "A_U18"  bus "0x01" dev "0x43" )
declare -A ps_chip_A_U100=( name "A_U100" bus "0x01" dev "0x46" )
declare -A ps_chip_U32=(    name "U32"    bus "0x02" dev "0x30" )
declare -A ps_chip_B_U26=(  name "B_U26"  bus "0x02" dev "0x40" )
declare -A ps_chip_B_U18=(  name "B_U18"  bus "0x02" dev "0x43" )
declare -A ps_chip_U34=(    name "U34"    bus "0x02" dev "0x43" )
declare -A ps_chip_B_U100=( name "B_U100" bus "0x02" dev "0x46" )

ps_chip=(ps_chip_U33 ps_chip_A_U26 ps_chip_A_U18 ps_chip_A_U100 ps_chip_U32 ps_chip_B_U26 ps_chip_B_U18 ps_chip_U34 ps_chip_B_U100)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Do test on Power Supply device
# Parameters:
# $1 - Power Supply chip information (name, bus, dev)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function ps_check_dev()
{
    local bus dev 
    declare -n chip_info="$1"

    bus="${chip_info[bus]}"
    dev="${chip_info[dev]}"
    
    echo -e "${C_YELLOW_B}"
    echo "*******************************************************"
    echo "* Testing Power Supply ${chip_info[name]}: Addr $dev on i2c bus $bus"
    echo "*******************************************************"
    echo -e -n "${C_NONE}"

    # --->>> Read Power Supply registers
    vset=$(i2cget -y -f $bus $dev $REG_PS_VSET)
    control1=$(i2cget -y -f $bus $dev $REG_PS_CONTROL1)
    control2=$(i2cget -y -f $bus $dev $REG_PS_CONTROL2)
    control3=$(i2cget -y -f $bus $dev $REG_PS_CONTROL3)
    status=$(i2cget -y -f $bus $dev $REG_PS_STATUS)
    echo -e "${C_BLUE_B}  >>> DEBUG: VSET=$vset, Control1=$control1, Control2=$control2, Control3=$control3, Status=$status${C_NONE}"
}
#####################################################
# ---->>>> Call tests for all devices...
for chip in "${ps_chip[@]}"; do
    ps_check_dev "$chip"
done
