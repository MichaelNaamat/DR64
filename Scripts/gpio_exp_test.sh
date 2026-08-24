#!/bin/bash

source ./script_defs.sh     # Include general definitions for all tests (colors, etc.)

# --->>> Register addresses for GPIO-expansion chips
declare -r REG_GPIO_DIN0="0x00"   
declare -r REG_GPIO_DIN1="0x01"
declare -r REG_GPIO_DOUT0="0x02"
declare -r REG_GPIO_DOUT1="0x03"
declare -r REG_GPIO_POL0="0x04"
declare -r REG_GPIO_POL1="0x05"
declare -r REG_GPIO_CONF0="0x06"
declare -r REG_GPIO_CONF1="0x07"

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
    local bus dev din0 din1 dout0 dout1 pol0 pol1 conf0 conf1
    declare -n chip_info="$1"

    bus=${chip_info[bus]}
    dev=${chip_info[dev]}

    echo -e "${C_YELLOW_B}"
    echo "*******************************************************"
    echo "* Testing GPIO ${chip_info[name]}: Addr $dev on i2c bus $bus"
    echo "*******************************************************"
    echo -e -n "${C_NONE}"
    din0=$(i2cget -y -f $bus $dev $REG_GPIO_DIN0)
    din1=$(i2cget -y -f $bus $dev $REG_GPIO_DIN1)
    dout0=$(i2cget -y -f $bus $dev $REG_GPIO_DOUT0)
    dout1=$(i2cget -y -f $bus $dev $REG_GPIO_DOUT1)
    pol0=$(i2cget -y -f $bus $dev $REG_GPIO_POL0)
    pol1=$(i2cget -y -f $bus $dev $REG_GPIO_POL1)
    conf0=$(i2cget -y -f $bus $dev $REG_GPIO_CONF0)
    conf1=$(i2cget -y -f $bus $dev $REG_GPIO_CONF1)

    echo "  DIN0=$din0, DIN1=$din1, DOUT0=$dout0, DOUT1=$dout1"
    echo "  POL0=$pol0, POL1=$pol1, CONF0=$conf0, CONF1=$conf1"
}

########################################################################################
# ---->>>> Call tests for all devices...
for chip in "${gpio_chip[@]}"; do
    gpio_check_dev "$chip"
done
    