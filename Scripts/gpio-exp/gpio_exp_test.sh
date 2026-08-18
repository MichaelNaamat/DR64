#!/bin/bash

# ----->>> Define GPIO-expention chips
declare -A gpio_chip_U103=( name "U103"  bus "0x04" dev "0x74" )
declare -A gpio_chip_U104=( name "U104"  bus "0x00" dev "0x75" )
declare -A gpio_chip_U146=( name "U146"  bus "0x00" dev "0x74" )

gpio_chip=(gpio_chip_U103 gpio_chip_U104 gpio_chip_U146)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Do test on GPIO-expansion device
# Parameters:
# $1 - GPIO-expansion chip information (name, bus, dev)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function gpio_check_dev()
{
    local bus dev 
    declare -n chip_info="$1"

    bus=${chip_info[bus]}
    dev=${chip_info[dev]}

    echo 
    echo "****************************************************"
    echo "* Testing $1: Addr $dev on i2c bus $bus"
    echo "****************************************************"
  
}

########################################################################################
# ---->>>> Call tests for all devices...
for chip in "${gpio_chip[@]}"; do
    gpio_check_dev "$chip"
done
    