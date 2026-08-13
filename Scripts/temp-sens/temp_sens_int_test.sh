#!/bin/bash

# --->>> Register definition
REG_TEMP="0x00"
REG_CR="0x01"
REG_TLOW="0x02"
REG_THIGH="0x03"
REG_OS="0x04"

# --->>> List of temperature chips (i2c bus & device)
i2c_bus=("0x00" "0x04" "0x04" "0x04" "0x04")
i2c_dev=("0x49" "0x48" "0x49" "0x4A" "0x4C")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Test 
# Parameters:
# $1 - Bus number
# $2 - Device number
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function read_temp_reg()
{
    local bus dev cur_temp t_low t_high 
    bus=$1
    dev=$2

    cur_temp=$(i2cget -y -f $bus $dev $REG_TEMP w)
    t_low=$(i2cget -y -f $bus $dev $REG_TLOW w)
    t_high=$(i2cget -y -f $bus $dev $REG_THIGH w)
    echo "Current: Temp=$cur_temp, T-Low=$t_low, T-High=$t_high"
}

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Test interrupt line for temp75b-q1 tempratur sensor 
# Parameters:
# $1 - Bus number
# $2 - Device number
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function check_temp75b_int()
{
    local bus dev cur_temp org_t_low org_t_high 
    bus=$1
    dev=$2
	
    # ---->>> Save original High/Low limit to restore at end of Test
    org_t_low=$(i2cget -y -f $bus $dev $REG_TLOW w)
    org_t_high=$(i2cget -y -f $bus $dev $REG_THIGH w)
	
    echo "*****************************************"
    echo "* Testing Temp Dev $dev on i2c bus $bus"
    echo "*****************************************"
	
    # --->>> Set Configuration Reg (0x01).:
    # OS (15)    = '0'
    # CR (13-14) = '00'  | 37Hz conversion rate (typ) (default)
    # FQ (11-12) = '00'  | 1 fault (default)
    # POL (10)   = '0'   | ALERT is active low (default)
    # TM  (9)    = '1'   | ALERT is in interrupt mode
    # SD  (8)    = '0'   | Device is in continuous conversion mode (default)
    # Mask: 0000 0010 = 0x02
    i2cset -y -f $bus $dev $REG_CR 0x02
      
    # --->>> Read current temperature from device (Addr=0x00) & High/Low limits
    read_temp_reg $bus $dev     # DEBUG & clear int line
    
    # --->>> Print int state
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    echo "Pre-test Int state: ${gpio_line:58:2}"

    # ============ T-High test: Set T-High to +5c (T-Low stay -40c)
    i2cset -y -f $bus $dev $REG_THIGH 0x0005 w

    # --->>> Print int state
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    echo -n "T-High Int state(${gpio_line:58:2}): "
    test "${gpio_line:58:2}" = "lo" && echo "Pass" || echo "*** FAIL"
    read_temp_reg $bus $dev     # DEBUG & clear int line

    # ============ T-Low test: Set T-Low to +60c & T-High to +65c)
    i2cset -y -f $bus $dev $REG_TLOW 0x003C w
    i2cset -y -f $bus $dev $REG_THIGH 0x0041 w

    # --->>> Print int state
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    echo -n "T-Low Int state(${gpio_line:58:2}): "
    test "${gpio_line:58:2}" = "lo" && echo "Pass" || echo "*** FAIL"

    # --->>> Restore original values of T-Low/T-High before moving to next device
    # DEBUG: Set T-High: +60c, T-Low: -40c
#    t_high="0x003C"
#    t_low="0x00D8"

    echo "Restoring Org T-Low: $t_low T-High: $t_high"
    i2cset -y -f $bus $dev $REG_TLOW $org_t_low w
    i2cset -y -f $bus $dev $REG_THIGH $org_t_high w 
    read_temp_reg $bus $dev     # DEBUG & clear int line

    # --->>> Re-test interrupt after restoring limits to normal values
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    echo "Post-test Int state: ${gpio_line:58:2}"
}
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Test interrupt line for temp75c-q1 tempratur sensor 
# Parameters:
# $1 - Bus number
# $2 - Device number
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function check_temp75c_int()
{
    local bus dev t_low t_high
    bus=$1
    dev=$2
    
    echo "*****************************************"
    echo "* Testing Temp Dev $dev on i2c bus $bus"
    echo "*****************************************"
	
    # --->>> Set Configuration Reg (0x01).:
    #  - OS  =  '1': Set 'One-Shot' mode 
    #  - FQ  = '00': Trigger ALERT adter 1 fault (defult)
    #  - POL =  '0': ALERT active Low (default)
    #  - TM  =  '1': ALERT in interrupt mode
    #  - SD  =  '0': Clear 'Shutdown Mode' 
    #  xx10 0010 = 0x22
    i2cset -y -f $bus $dev $REG_CR 0x22
    
    # --->>> Write 'One-Shot' register to start conversion (Addr=0x04) (suppress errors)
    i2cset -y -f $bus $dev $REG_OS 0x00 >/dev/null 2>&1
    
    # --->>> Read current temperature from device (Addr=0x00)
    echo -n "Current Temp: "
    i2cget -y -f $bus $dev $REG_TEMP w
    
    # --->>> Read original values of T-Low/T-High for restoration after test
    t_low=$(i2cget -y -f $bus $dev 0x02 w)
    t_high=$(i2cget -y -f $bus $dev 0x03 w)
	
    # --->>> Set T-Low Temp limit (Addr 0x02) to 1c
    i2cset -y -f $bus $dev $REG_TLOW 0x0001 w
    
    # --->>> Set T-High Temp limit (Addr 0x03) to 5c
    i2cset -y -f $bus $dev $REG_HIGH 0x0005 w
    
    # --->>> Write 'One-Shot' register to start conversion (Addr=0x04) (suppress errors)
    i2cset -y -f $bus $dev $REG_OS 0x00>/dev/null 2>&1
    
    # --->>> Re-read values of T-Low/T-High
    echo -n "T-Low: "
    i2cget -y -f $bus $dev $REG_TLOW w
    
    echo -n "T-High: "
    i2cget -y -f $bus $dev $REG_THIGH w
    
    # --->>> Read GPIO to see if interrupt is activated
    # "gpio-357 (PC_04               |AViVA               ) in  lo IRQ"
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    echo "Int state: ${gpio_line:58:2}"
    test "${gpio_line:58:2}" = "lo" && echo ">>> Test Pass" || echo "*** Test FAIL ***"

    # --->>> Restore original values of T-Low/T-High before moving to next device
    # DEBUG: Set T-High: 60c, T-Low: 58c
    t_high="0x003C"
    t_low="0x003A"

    echo "Restoring Org T-Low: $t_low T-High: $t_high"
    i2cset -y -f $bus $dev $REG_TLOW $t_low w
    i2cset -y -f $bus $dev $REG_THIGH $t_high w 

    # --->>> Re-test interrupt after restoring limits to normal values
    i2cset -y -f $bus $dev $REG_OS 0x00>/dev/null 2>&1
    gpio_line=$(cat  /sys/kernel/debug/gpio | grep "PC_04")
    echo "Normal Int state: ${gpio_line:58:2}"
}

# ---->>>> Call tests for all devices...
for i in {0..4}
do
    check_temp75b_int ${i2c_bus[$i]} ${i2c_dev[$i]}
done

