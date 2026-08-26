#!/bin/bash

source ./script_defs.sh     # Include general definitions for all tests (colors, etc.)

# -------------------- Bank independent ------------------------
declare -r REG_BANK_SEL="0xF0"

# -------------------- Bank 0 registers ------------------------
# --->>> Reg addresses of MON_LVL[i] for channels 0..7
declare -a REG_VMON_LVL=("0x40" "0x41" "0x42" "0x43" "0x44" "0x45" "0x46" "0x47")   

# -------------------- Bank 1 registers ------------------------
declare -r REG_IEN_UVHF="0x13"   # Interrupt enable for Under Voltage High-Frequency
declare -r REG_IEN_UVLF="0x14"   # Interrupt enable for Under Voltage Low-Frequency
declare -r REG_IEN_OVHF="0x15"   # Interrupt enable for Over Voltage High-Frequency
declare -r REG_IEN_OVLF="0x16"   # Interrupt enable for Over Voltage Low-Frequency

declare -r REG_MON_CH_EN="0x1E"   # Monitor channel enable
declare -r REG_VRANGE_MULT="0x1F"   

# --->>> Under/Over voltage threshold registers for channels 0..7
declare -a REG_UV_HF=("0x20" "0x30" "0x40" "0x50" "0x60" "0x70" "0x80" "0x90")   # UV_HF[i] for channels 0..7
declare -a REG_OV_HF=("0x21" "0x31" "0x41" "0x51" "0x61" "0x71" "0x81" "0x91")   # OV_HF[i] for channels 0..7
declare -a REG_UV_LF=("0x22" "0x32" "0x42" "0x52" "0x62" "0x72" "0x82" "0x92")   # UV_LF[i] for channels 0..7
declare -a REG_OV_LF=("0x23" "0x33" "0x43" "0x53" "0x63" "0x73" "0x83" "0x93")   # OV_LF[i] for channels 0..7


declare -A U93_ch1=(name "0.875V (core) +2.5% / -3%" min 0.84875 typ 0.875  max 0.896875)
declare -A U93_ch2=(name "1.8V (PCIE) +/-5%"         min 1.71    typ 1.8    max 1.89)
declare -A U93_ch3=(name "1.8V (IP) +/-3%"           min 1.746   typ 1.8    max 1.854)
declare -A U93_ch4=(name "0.86V (PCIE) +/-5%"        min 0.817   typ 0.86   max 0.903)
declare -A U93_ch5=(name "0.75V (MIPI) +/-5%"        min 0.7125  typ 0.75   max 0.7875)
declare -A U93_ch6=(name "1.05V (DDR) +/-3%"         min 1.0185  typ 1.05   max 1.0815)
declare -A U93_ch7=(name "0.5V (DDR) +/-5%"          min 0.475   typ 0.5    max 0.525)
declare -A U93_ch8=(name "1.8V (Main) +/-5%"         min 1.71    typ 1.8    max 1.89)
declare -a U93_channels=(U93_ch1 U93_ch2 U93_ch3 U93_ch4 U93_ch5 U93_ch6 U93_ch7 U93_ch8)

declare -A U94_ch1=(name "0.875V (core) +2.5% / -3%" min 0.84875 typ 0.875  max 0.896875)
declare -A U94_ch2=(name "1.8V (PCIE) +/-5%"         min 1.71    typ 1.8    max 1.89)
declare -A U94_ch3=(name "1.8V (IP) +/-3%"           min 1.746   typ 1.8    max 1.854)
declare -A U94_ch4=(name "0.86V (PCIE) +/-5%"        min 0.817   typ 0.86   max 0.903)
declare -A U94_ch5=(name "0.75V (MIPI) +/-5%"        min 0.7125  typ 0.75   max 0.7875)
declare -A U94_ch6=(name "1.05V (DDR) +/-3%"         min 1.0185  typ 1.05   max 1.0815)
declare -A U94_ch7=(name "0.5V (DDR) +/-5%"          min 0.475   typ 0.5    max 0.525)
declare -A U94_ch8=(name "1.8V (Main) +/-5%"         min 1.71    typ 1.8    max 1.89)
declare -a U94_channels=(U94_ch1 U94_ch2 U94_ch3 U94_ch4 U94_ch5 U94_ch6 U94_ch7 U94_ch8)

declare -A U95_ch1=(name "1.1V (USS_12v_M) +/-5%"   min 1.03835 typ 1.1     max 1.14765)
declare -A U95_ch2=(name "5V (5V_CAN) +/-5%"        min 4.75    typ 5       max 5.25)
declare -A U95_ch3=(name "1.2V (DES_1v2) +/-5%"     min 1.14    typ 1.2     max 1.26)
declare -A U95_ch4=(name "1.2V (5V_AOLDO_M) +/-5%"  min 1.12575 typ 1.185   max 1.24425)
declare -A U95_ch5=(name "0.8V (DES_0V8) +/-5%"     min 0.76    typ 0.8     max 0.84)
declare -A U95_ch6=(name "3.3V (3V3) +/-5%"         min 3.135   typ 3.3     max 3.465)
declare -A U95_ch7=(name "1.1V (12vPoC_M) +/-5%"    min 1.03835 typ 1.1     max 1.14765)
declare -A U95_ch8=(name "5V"                       min 4.75    typ 5       max 5.25)
declare -a U95_channels=(U95_ch1 U95_ch2 U95_ch3 U95_ch4 U95_ch5 U95_ch6 U95_ch7 U95_ch8)
    
declare -A U114_ch1=(name "0.8V () +/-5%"           min 0.76    typ 0.8  max 0.84)
declare -A U114_ch2=(name "1.2V () +/-5%"           min 1.14    typ 1.2  max 1.26)
declare -A U114_ch3=(name "0.8V () +/-5%"           min 0.76    typ 0.8  max 0.84)
declare -A U114_ch4=(name "1.2V () +/-5%"           min 1.14    typ 1.2  max 1.26)
declare -A U114_ch5=(name "0.84V () +/-5%"          min 0.798   typ 0.84 max 0.882)
declare -A U114_ch6=(name "1.2V () +/-5%"           min 1.14    typ 1.2  max 1.26)
declare -A U114_ch7=(name "1.8V (ETH_1v8) +/-5%"    min 1.71    typ 1.8  max 1.89)
declare -A U114_ch8=(name "5V (Main 5V) +/-5%"      min 4.75    typ 5    max 5.25)
declare -a U114_channels=(U114_ch1 U114_ch2 U114_ch3 U114_ch4 U114_ch5 U114_ch6 U114_ch7 U114_ch8)
    
declare -A U148_ch1=(name "0.8V (TDA4_0v8_VDD_CORE) +/-5%"   min 0.76    typ 0.8     max 0.84)
declare -A U148_ch2=(name "0.8V (TDA4_0v8_CPU_AVS) +/-5%"    min 0.76    typ 0.8     max 0.84)
declare -A U148_ch3=(name "1.1V (TDA4_1v1) +/-5%"            min 1.045   typ 1.1     max 1.155)
declare -A U148_ch4=(name "0.85V (TDA4_0v85) +/-5%"          min 0.8075  typ 0.85    max 0.8925)
declare -A U148_ch5=(name "1.8V (TDA4_1v8_PHY_LDO) +/-5%"    min 1.71    typ 1.8     max 1.89)
declare -A U148_ch6=(name "0.8V (TDA4_0v8_DLL_LDO) +/-5%"    min 0.76    typ 0.8     max 0.84)
declare -A U148_ch7=(name "1.8V (TDA4_1v8_PLL_LDO) +/-5%"    min 1.71    typ 1.8     max 1.89)
## declare -A U148_ch8=(name "0V disabled"                      min 0       typ 0       max 0)
declare -a U148_channels=(U148_ch1 U148_ch2 U148_ch3 U148_ch4 U148_ch5 U148_ch6 U148_ch7 U148_ch8)

# ----->>> Define VMON chips and their channels
declare -A vmon_chip_U93=( name "U93"  bus "0x00" dev "0x37" channels U93_channels)
declare -A vmon_chip_U94=( name "U94"  bus "0x00" dev "0x36" channels U94_channels)
declare -A vmon_chip_U95=( name "U95"  bus "0x00" dev "0x35" channels U95_channels)
declare -A vmon_chip_U114=(name "U114" bus "0x00" dev "0x34" channels U114_channels)
declare -A vmon_chip_U148=(name "U148" bus "0x04" dev "0x33" channels U148_channels)  # ** Conflict on bus number

vmon_chip=(vmon_chip_U93 vmon_chip_U94 vmon_chip_U95 vmon_chip_U114) # vmon_chip_U148)

# ---->>> Program command line parameters for all VMON devices
declare -r CL_PAR1=$1

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Get value (0/1) of a GPIO pin
# Parameters:
# $1 - GPIO pin identifier
# Return: 0 or 1
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function vmon_get_pin()
{
    local cmd_out

    cmd_out=$(wget -qO- --method=POST \
                   --header='accept: application/json' \
                   --header='Content-Type: application/json' \
                   --body-data='{"log_level": "INFO", "gpios": ["'"$1"'"]}' \
                   "http://10.0.0.102:8000/controller/gpio/read_values/"))

    return ${cmd_out:129:1}
}

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Test values of voltage monitor registers for a given device
# Parameters:
# $1 - Bus number
# $2 - Device number
# $3 - Monitor channel (0..7)
# $4 - Channel information (name, min, typ, max)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function vmon_check_channel()
{
    local bus dev ch
    local ch_info
    local mon_lvl uv_hf ov_hf uv_lf ov_lf  # row data read from H/W registers
    local mon_lvl_v uv_hf_v ov_hf_v uv_lf_v ov_lf_v  # registers data convertad to voltage values
    local min_val typ_val max_val          # Min/typ/max values for channel $ch
    local coef mul                         # To convert ADC value to voltage

    local int_stat1 int_stat2 int_stat3   # State of interrupt: Before, during, after test

    bus=$1
    dev=$2
    ch=$3
    declare -n ch_info="$4"
    coef=$5
    mul=$6

    # --->>> Read min/typ/max values for channel $ch
    min_val=${ch_info[min]}
    typ_val=${ch_info[typ]}
    max_val=${ch_info[max]}

    # ---->>>> Read channel data from H/W
    i2cset -y -f $bus $dev $REG_BANK_SEL 0x00   # Select Bank 0    
    mon_lvl=$(i2cget -y -f $bus $dev ${REG_VMON_LVL[$ch]})

    i2cset -y -f $bus $dev $REG_BANK_SEL 0x01   # Select Bank 1
    uv_hf=$(i2cget -y -f $bus $dev ${REG_UV_HF[$ch]})
    ov_hf=$(i2cget -y -f $bus $dev ${REG_OV_HF[$ch]})
    uv_lf=$(i2cget -y -f $bus $dev ${REG_UV_LF[$ch]})
    ov_lf=$(i2cget -y -f $bus $dev ${REG_OV_LF[$ch]})

    mon_lvl=$(($mon_lvl))
    uv_hf=$(($uv_hf))
    ov_hf=$(($ov_hf))
    uv_lf=$(($uv_lf))
    ov_lf=$(($ov_lf))

 #   mon_lvl=$((0x10))  # For testing, assume max level

    # --->>> Check if monitor level is within valid range (0..255)
    if (( $mon_lvl <= 0 || $mon_lvl > 255 )); then
        echo -e "${C_RED_B}  >>> ERROR: Invalid monitor level ($mon_lvl) for channel ${ch}${C_NONE}"
        return
    fi

    if [[ "$CL_PAR1" == "debug" ]]; then
        # --->>> Calculate voltage value for channel $ch according to H/W value
        mon_lvl_v=$(awk -v a="$mon_lvl" -v coef="$coef" -v mul="$mul" 'BEGIN { printf "%.3f", coef + a * mul }')
        uv_hf_v=$(awk -v a="$uv_hf" -v coef="$coef" -v mul="$mul" 'BEGIN { printf "%.3f", coef + a * mul }')
        ov_hf_v=$(awk -v a="$ov_hf" -v coef="$coef" -v mul="$mul" 'BEGIN { printf "%.3f", coef + a * mul }')
        uv_lf_v=$(awk -v a="$uv_lf" -v coef="$coef" -v mul="$mul" 'BEGIN { printf "%.3f", coef + a * mul }')
        ov_lf_v=$(awk -v a="$ov_lf" -v coef="$coef" -v mul="$mul" 'BEGIN { printf "%.3f", coef + a * mul }')

        echo -e "${C_BLUE_B}  >>> DEBUG: Ch ${ch}: min=$min_val, typ=$typ_val, max=$max_val, MON_LVL=$mon_lvl_v($mon_lvl)"
        echo -e "                             UV_HF=$uv_hf_v($uv_hf) OV_HF=$ov_hf_v($ov_hf) UV_LF=$uv_lf_v($uv_lf) OV_LF=$ov_lf_v($ov_lf)${C_NONE}"

        # ---->>> Check if voltage value is within min/max range
        if (( $(awk -v x="$mon_lvl_v" -v min="$min_val" 'BEGIN { print (x < min) }') )); then
            echo -e "${C_RED}  >>> Ch ${ch}: ERROR: Less than min ($mon_lvl_v < $min_val)${C_NONE}"
        elif (( $(awk -v x="$mon_lvl_v" -v max="$max_val" 'BEGIN { print (x > max) }') )); then
            echo -e "${C_RED}  >>> Ch ${ch}: ERROR: More than max ($mon_lvl_v > $max_val)${C_NONE}"
        else
            echo -e "${C_GREEN}  >>> Ch ${ch}: OK: $mon_lvl_v is within range [$min_val, $max_val]${C_NONE}"
        fi
    fi

    # ---------------------->>> Check UV interrupt <<<---------------------
    int_stat1=$(vmon_get_pin "PK_08")

    i2cset -y -f $bus $dev ${REG_UV_HF[$ch]} $ov_hf             # Set UV_HF to value of OV to trigger UV interrupt
    int_stat2=$(vmon_get_pin "PK_08")     # Read int (pk_07 GPIO) state during test

    i2cset -y -f $bus $dev ${REG_UV_HF[$ch]} $uv_hf             # Restore original UV_HF value
    int_stat3=$(vmon_get_pin "PK_08")     # Read int (pk_07 GPIO)

    echo -n "  >>> Ch ${ch}: UV interrupt state: Before(${int_stat1}), During(${int_stat2}), After(${int_stat3}): "
    test "$int_stat1" = "0" && echo -e -n "${C_RED_B}FAIL,${C_NONE}" || echo -e -n "${C_GREEN_B}Pass,${C_NONE}"
    test "$int_stat2" = "1" && echo -e -n "${C_RED_B}FAIL,${C_NONE}" || echo -e -n "${C_GREEN_B}Pass,${C_NONE}"
    test "$int_stat3" = "0" && echo -e -n "${C_RED_B}FAIL${C_NONE}"  || echo -e -n "${C_GREEN_B}Pass${C_NONE}"
    echo

    # ---------------------->>> Check OV interrupt <<<---------------------
    int_stat1=$(vmon_get_pin "PK_08")     # Read int (pk_07 GPIO) state before test

    i2cset -y -f $bus $dev ${REG_OV_HF[$ch]} $uv_hf             # Set OV_HF to value of UV to trigger OV interrupt
    int_stat2=$(vmon_get_pin "PK_08")     # Read int (pk_07 GPIO) state during test

    i2cset -y -f $bus $dev ${REG_OV_HF[$ch]} $ov_hf             # Restore original OV_HF value
    int_stat3=$(vmon_get_pin "PK_08")     # Read int (pk_07 GPIO)

    echo -n "  >>> Ch ${ch}: OV interrupt state: Before(${int_stat1}), During(${int_stat2}), After(${int_stat3}): "
    test "$int_stat1" = "0" && echo -e -n "${C_RED_B}FAIL,${C_NONE}" || echo -e -n "${C_GREEN_B}Pass,${C_NONE}"
    test "$int_stat2" = "1" && echo -e -n "${C_RED_B}FAIL,${C_NONE}" || echo -e -n "${C_GREEN_B}Pass,${C_NONE}"
    test "$int_stat3" = "0" && echo -e -n "${C_RED_B}FAIL${C_NONE}"  || echo -e -n "${C_GREEN_B}Pass${C_NONE}"
    echo
}
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Do test on VMON device
# Parameters:
# $1 - VMON chip information (name, bus, dev)
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
function vmon_check_dev()
{
    local bus dev chlist ch_ind ch
    local vrange_mult
    local ien_uvhf ien_ovhf ien_uvlf ien_ovlf mon_ch_en  # Interrupt enable bits for channel $ch
 
    declare -n chip_info="$1"

    bus=${chip_info[bus]}
    dev=${chip_info[dev]}
    declare -n chlist=${chip_info[channels]}

    # Read mask of channel multiplaction (x1/x4) for this device
    i2cset -y -f $bus $dev $REG_BANK_SEL 0x01   # Select Bank 1
    vrange_mult=$(i2cget -y -f $bus $dev $REG_VRANGE_MULT)
    vrange_mult=$(($vrange_mult))

    echo -e "${C_YELLOW}"
    echo -e "****************************************************"
    echo -e "* Testing $1: Addr $dev on i2c bus $bus *"
    if [[ "$CL_PAR1" == "debug" ]]; then
        ien_uvhf=$(i2cget -y -f $bus $dev $REG_IEN_UVHF)   # Interrupt enable for Under Voltage High-Frequency
        ien_uvlf=$(i2cget -y -f $bus $dev $REG_IEN_UVLF)   # Interrupt enable for Under Voltage Low-Frequency
        ien_ovhf=$(i2cget -y -f $bus $dev $REG_IEN_OVHF)   # Interrupt enable for Over Voltage High-Frequency
        ien_ovlf=$(i2cget -y -f $bus $dev $REG_IEN_OVLF)   # Interrupt enable for Over Voltage Low-Frequency
        mon_ch_en=$(i2cget -y -f $bus $dev $REG_MON_CH_EN)   # Monitor channel enable
        echo -e "* Int enable: UVHF=$ien_uvhf, UVLF=$ien_uvlf, OVHF=$ien_ovhf, OVLF=$ien_ovlf, MON_CH_EN=$mon_ch_en *"
    fi
    echo -e "****************************************************${C_NONE}"
    
    # --->>> Loop over channels and test each one
    ch_ind=0
    for ch in "${chlist[@]}"; do
        declare -n vmon_ch="$ch"
        if [[ -z ${vmon_ch[name]} ]]; then   # Skip non-active channels (e.g. U148_ch8)
            continue
        fi

        if (((vrange_mult & (1 << $ch_ind)) != 0)); then
            vmon_check_channel "$bus" "$dev" "$ch_ind" "$ch" "0.8"  "0.020" # x4 range
        else
            vmon_check_channel "$bus" "$dev" "$ch_ind" "$ch" "0.2"  "0.005" # x1 range
        fi
        ch_ind=$((ch_ind + 1))
    done
}

########################################################################################
# ---->>>> Call tests for all devices...
for chip in "${vmon_chip[@]}"; do
    vmon_check_dev "$chip"
done    
