#!/bin/bash

source ./script_defs.sh     # Include general definitions for all tests (colors, etc.)

# --->>> Register definition
declare -r REG_TEMP="0x00"
declare -r REG_CR="0x01"
declare -r REG_TLOW="0x02"
declare -r REG_THIGH="0x03"
declare -r REG_OS="0x04"

# ----->>> Define Temp-sensor chips
declare -A temp_chip_U60=(  name "U60"   bus "0x04" dev "0x48" )
declare -A temp_chip_U61=(  name "U61"   bus "0x04" dev "0x4C" )
declare -A temp_chip_U62=(  name "U62"   bus "0x04" dev "0x49" )
declare -A temp_chip_U64=(  name "U64"   bus "0x04" dev "0x4A" )
declare -A temp_chip_U127=( name "U127"  bus "0x00" dev "0x49" )

temp_chip=(temp_chip_U60 temp_chip_U61 temp_chip_U62 temp_chip_U64 temp_chip_U127)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Test interrupt line for temp75b-q1 tempratur sensor 
# Parameters:
# $1 - Temperature sensor chip associative array (name, bus, dev)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function temp75b_check_int()
{
    local bus dev cur_temp org_t_low org_t_high 
    local chip_info
    local int_before int_during int_after
    local cur_temp t_low t_high 

    declare -n chip_info="$1"

    bus=${chip_info[bus]}
    dev=${chip_info[dev]}
	
    # ---->>> Save original High/Low limit to restore at end of Test
    org_t_low=$(i2cget -y -f $bus $dev $REG_TLOW w)
    org_t_high=$(i2cget -y -f $bus $dev $REG_THIGH w)
	
    echo -e "${C_YELLOW_B}"
    echo   "****************************************************"
    echo   "* Testing Temp Sens ${chip_info[name]}: Addr $dev on i2c bus $bus"
    printf "* T-Low=%uc, T-High=%uc\n" "$org_t_low" "$org_t_high"
    echo   "****************************************************"
    echo -e -n "${C_NONE}"
    sleep 0.1
	
    # --->>> Set Configuration Reg (0x01):
    # OS (15)    = '0'
    # CR (13-14) = '00'  | 37Hz conversion rate (typ) (default)
    # FQ (11-12) = '00'  | 1 fault (default)
    # POL (10)   = '0'   | ALERT is active low (default)
    # TM  (9)    = '0'   | ALERT is in comperator mode (default)
    # SD  (8)    = '0'   | Device is in continuous conversion mode (default)
    # Mask: 0000 0000 = 0x00
    i2cset -y -f $bus $dev $REG_CR 0x00
         
    # ============ T-High test: Set T-High to +5c, T-Low to +2
    # --->>> Save int state
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    int_before=${gpio_line:58:2}

    i2cset -y -f $bus $dev $REG_THIGH +5 w    # Set T-High to +5c
    i2cset -y -f $bus $dev $REG_TLOW +2 w    # Set T-Low to +2c

    # --->>> Save int state
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    int_during=${gpio_line:58:2}

    # --->>> Read T-Low/T-High values & clear interrupt
    t_low=$(i2cget -y -f $bus $dev $REG_TLOW w)
    t_high=$(i2cget -y -f $bus $dev $REG_THIGH w)

    # --->>> Restor normal values 
    i2cset -y -f $bus $dev $REG_TLOW $org_t_low w
    i2cset -y -f $bus $dev $REG_THIGH $org_t_high w

    # --->>> Read current temperature
    cur_temp=$(i2cget -y -f $bus $dev $REG_TEMP w)
    cur_temp=$(($cur_temp&0xFF))   # Take only the integer degrees
 
    # --->>> Save int state
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    int_after=${gpio_line:58:2}
    
    # ---->>> Print results of interrupt test
    printf "  T-High/T-Low test: Temp=%uc, T-Low=%uc, T-High=%uc, Before($int_before), During($int_during), After($int_after) - " "$cur_temp" "$t_low" "$t_high"
    test "$int_before" = "hi" && echo -e -n "${C_GREEN_B}Pass,${C_NONE}" || echo -e -n "${C_RED_B}FAIL,${C_NONE}"
    test "$int_during" = "lo" && echo -e -n "${C_GREEN_B}Pass,${C_NONE}" || echo -e -n "${C_RED_B}FAIL,${C_NONE}"
    test "$int_after" = "hi" && echo -e "${C_GREEN_B}Pass,${C_NONE}" || echo -e "${C_RED_B}FAIL,${C_NONE}"
}
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Test interrupt line for temp75c-q1 tempratur sensor 
# Parameters:
# $1 - Bus number
# $2 - Device number
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## TBDfunction temp75c_check_int()
## TBD{
## TBD    local bus dev t_low t_high
## TBD    bus=$1
## TBD    dev=$2
## TBD    
## TBD    echo "*****************************************"
## TBD    echo "* Testing Temp Dev $dev on i2c bus $bus"
## TBD    echo "*****************************************"
## TBD	
## TBD    # --->>> Set Configuration Reg (0x01).:
## TBD    #  - OS  =  '1': Set 'One-Shot' mode 
## TBD    #  - FQ  = '00': Trigger ALERT adter 1 fault (defult)
## TBD    #  - POL =  '0': ALERT active Low (default)
## TBD    #  - TM  =  '1': ALERT in interrupt mode
## TBD    #  - SD  =  '0': Clear 'Shutdown Mode' 
## TBD    #  xx10 0010 = 0x22
## TBD    i2cset -y -f $bus $dev $REG_CR 0x22
## TBD    
## TBD    # --->>> Write 'One-Shot' register to start conversion (Addr=0x04) (suppress errors)
## TBD    i2cset -y -f $bus $dev $REG_OS 0x00 >/dev/null 2>&1
## TBD    
## TBD    # --->>> Read current temperature from device (Addr=0x00)
## TBD    echo -n "Current Temp: "
## TBD    i2cget -y -f $bus $dev $REG_TEMP w
## TBD    
## TBD    # --->>> Read original values of T-Low/T-High for restoration after test
## TBD    t_low=$(i2cget -y -f $bus $dev 0x02 w)
## TBD    t_high=$(i2cget -y -f $bus $dev 0x03 w)
## TBD	
## TBD    # --->>> Set T-Low Temp limit (Addr 0x02) to 1c
## TBD    i2cset -y -f $bus $dev $REG_TLOW 0x0001 w
## TBD    
## TBD    # --->>> Set T-High Temp limit (Addr 0x03) to 5c
## TBD    i2cset -y -f $bus $dev $REG_HIGH 0x0005 w
## TBD    
## TBD    # --->>> Write 'One-Shot' register to start conversion (Addr=0x04) (suppress errors)
## TBD    i2cset -y -f $bus $dev $REG_OS 0x00>/dev/null 2>&1
## TBD    
## TBD    # --->>> Re-read values of T-Low/T-High
## TBD    echo -n "T-Low: "
## TBD    i2cget -y -f $bus $dev $REG_TLOW w
## TBD    
## TBD    echo -n "T-High: "
## TBD    i2cget -y -f $bus $dev $REG_THIGH w
## TBD    
## TBD    # --->>> Read GPIO to see if interrupt is activated
## TBD    # "gpio-357 (PC_04               |AViVA               ) in  lo IRQ"
## TBD    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
## TBD    echo "Int state: ${gpio_line:58:2}"
## TBD    test "${gpio_line:58:2}" = "lo" && echo -e "${C_GREEN}>>> Test Pass${C_NONE}" || echo -e "${C_RED}*** Test FAIL ***${C_NONE}"
## TBD
## TBD    # --->>> Restore original values of T-Low/T-High before moving to next device
## TBD    # DEBUG: Set T-High: 60c, T-Low: 58c
## TBD    t_high="0x003C"
## TBD    t_low="0x003A"
## TBD
## TBD    echo "Restoring Org T-Low: $t_low T-High: $t_high"
## TBD    i2cset -y -f $bus $dev $REG_TLOW $t_low w
## TBD    i2cset -y -f $bus $dev $REG_THIGH $t_high w 
## TBD
## TBD    # --->>> Re-test interrupt after restoring limits to normal values
## TBD    i2cset -y -f $bus $dev $REG_OS 0x00>/dev/null 2>&1
## TBD    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
## TBD    echo "Normal Int state: ${gpio_line:58:2}"
## TBD}

############################################################################
# ---->>>> Call tests for all devices...
for chip in "${temp_chip[@]}"; do
    temp75b_check_int "$chip"
done

