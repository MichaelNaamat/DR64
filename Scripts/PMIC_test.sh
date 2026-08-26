#!/bin/bash

source ./script_defs.sh     # Include general definitions for all tests (colors, etc.)

# --->>> Register addresses for GPIO-expansion chips
declare -r REG_PMIC_DEVICEID="0x2B"        # Device ID

# ----->>> Define PMIC chips
declare -A pmic_chip_U54_A=( name "U54"  bus "0x04" dev "0x20" )
declare -A pmic_chip_U54_B=( name "U54"  bus "0x04" dev "0x21" )

pmic_chip=(pmic_chip_U54_A pmic_chip_U54_B)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Do test on PMIC device
# Parameters:
# $1 - PMIC chip information (name, bus, dev)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function pmic_check_dev()
{
    local bus dev dev_id
    declare -n chip_info="$1"

    bus=${chip_info[bus]}
    dev=${chip_info[dev]}

    echo -e "${C_YELLOW_B}"
    echo "*******************************************************"
    echo "* Testing PMIC ${chip_info[name]}: Addr $dev on i2c bus $bus"
    echo "*******************************************************"
    echo -e -n "${C_NONE}"

    # --->>> Read PMIC registers
    dev_id=$(i2cget -y -f $bus $dev $REG_PMIC_DEVICEID w)       # read Device ID register (16-bit value)
    echo -e "${C_BLUE_B}  >>> DEBUG: Device ID=$dev_id${C_NONE}"
}
########################################################################################
# ---->>>> Call tests for all devices...
for chip in "${pmic_chip[@]}"; do
    pmic_check_dev "$chip"
done
