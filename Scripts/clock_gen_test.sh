#!/bin/bash

source ./script_defs.sh     # Include general definitions for all tests (colors, etc.)

# --->>> Register addresses for GPIO-expansion chips
declare -r REG_CLK_DEVICE_PN_BASE "0x0D"        # Device PN
declare -r REG_CLK_DEVICE_REV     "0x0E"        # Device Revision

# ----->>> Define Clock-Gen chips
declare -A clock_gen_chip_U87=( name "U87"  bus "0x01" dev "0x6A" )
declare -A clock_gen_chip_U88=( name "U88"  bus "0x01" dev "0x6B" )

clock_gen_chip=(clock_gen_chip_U87 clock_gen_chip_U88)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Do test on Clock-Gen device
# Parameters:
# $1 - Clock-Gen chip information (name, bus, dev)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function clock_gen_check_dev()
{
    local bus dev 
    local dev_pn dev_rev
    declare -n chip_info="$1"

    bus=${chip_info[bus]}
    dev=${chip_info[dev]}

    echo -e "${C_YELLOW_B}"
    echo "*******************************************************"
    echo "* Testing Clock-Gen ${chip_info[name]}: Addr $dev on i2c bus $bus"
    echo "*******************************************************"
    echo -e -n "${C_NONE}"

    # --->>> Read Clock-Gen registers
    dev_pn=$(i2cget -y -f $bus $dev $REG_CLK_DEVICE_PN_BASE)
    dev_rev=$(i2cget -y -f $bus $dev $REG_CLK_DEVICE_REV)
    echo -e "${C_BLUE_B}  >>> DEBUG: Device PN=$dev_pn, Device REV=$dev_rev${C_NONE}"
}
######################################################
# ---->>>> Call tests for all devices...
for chip in "${clock_gen_chip[@]}"; do
    clock_gen_check_dev "$chip"
done    