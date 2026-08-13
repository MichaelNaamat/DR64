#!/bin/bash
echo -e "____________________________________________________________"
echo -e ""
echo -e "I2C BSP Test Library, Version 1.0.0.0"
echo -e "Written by Arsen Sogomonyan, Copyright (C) 2026"
echo -e "____________________________________________________________"
echo -e ""

function i2cdetect_usage()
{
echo -e "Usage: i2cdetect [-y] [-a] [-q|-r] I2CBUS [FIRST LAST]"
echo -e "       i2cdetect -F I2CBUS"
echo -e "       i2cdetect -l"
echo -e "  I2CBUS is an integer or an I2C bus name"
echo -e "  If provided, FIRST and LAST limit the probing range."
echo
}

function i2cdump_usage()
{
echo -e "Usage: i2cdump [-f] [-y] [-r first-last] [-a] I2CBUS ADDRESS [MODE [BANK [BANKREG]]]"
echo -e "  I2CBUS is an integer or an I2C bus name"
echo -e "  ADDRESS is an integer (0x08 - 0x77, or 0x00 - 0x7f if -a is given)"
echo -e "  MODE is one of:"
echo -e "    b (byte, default)"
echo -e "    w (word)"
echo -e "    W (word on even register addresses)"
echo -e "    s (SMBus block, deprecated)"
echo -e "    i (I2C block)"
echo -e "    c (consecutive byte)"
echo -e "    Append p for SMBus PEC"
echo
}

function i2cget_usage()
{
echo -e "Usage: i2cget [-f] [-y] [-a] I2CBUS CHIP-ADDRESS [DATA-ADDRESS [MODE [LENGTH]]]"
echo -e "  I2CBUS is an integer or an I2C bus name"
echo -e "  ADDRESS is an integer (0x08 - 0x77, or 0x00 - 0x7f if -a is given)"
echo -e "  MODE is one of:"
echo -e "    b (read byte data, default)"
echo -e "    w (read word data)"
echo -e "    c (write byte/read byte)"
echo -e "    s (read SMBus block data)"
echo -e "    i (read I2C block data)"
echo -e "    Append p for SMBus PEC"
echo -e "  LENGTH is the I2C block data length (between 1 and 32, default 32)"
echo
}

function i2cset_usage()
{
echo -e "Usage: i2cset [-f] [-y] [-m MASK] [-r] [-a] I2CBUS CHIP-ADDRESS DATA-ADDRESS [VALUE] ... [MODE]"
echo -e "  I2CBUS is an integer or an I2C bus name"
echo -e "  ADDRESS is an integer (0x08 - 0x77, or 0x00 - 0x7f if -a is given)"
echo -e "  MODE is one of:"
echo -e "    c (byte, no value)"
echo -e "    b (byte data, default)"
echo -e "    w (word data)"
echo -e "    i (I2C block data)"
echo -e "    s (SMBus block data)"
echo -e "    Append p for SMBus PEC"
echo
}

function i2ctransfer_usage()
{
echo -e "Usage: i2ctransfer [-f] [-y] [-v] [-V] [-a] I2CBUS DESC [DATA] [DESC [DATA]]..."
echo -e "  I2CBUS is an integer or an I2C bus name"
echo -e "  DESC describes the transfer in the form: {r|w}LENGTH[@address]"
echo -e "    1) read/write-flag 2) LENGTH (range 0-65535, or '?')"
echo -e "    3) I2C address (use last one if omitted)"
echo -e "  DATA are LENGTH bytes for a write message. They can be shortened by a suffix:"
echo -e "    = (keep value constant until LENGTH)"
echo -e "    + (increase value by 1 until LENGTH)"
echo -e "    - (decrease value by 1 until LENGTH)"
echo -e "    p (use pseudo random generator until LENGTH with value as seed)"
echo
echo -e "Example (bus 0, read 8 byte at offset 0x64 from EEPROM at 0x50):"
echo -e "  # i2ctransfer 0 w1@0x50 0x64 r8"
echo -e "Example (same EEPROM, at offset 0x42 write 0xff 0xfe ... 0xf0):"
echo -e "  # i2ctransfer 0 w17@0x50 0x42 0xff-"
echo
}

function try()
{
	local name=$1
	shift
	if [ -z "$1" ] ; then
		echo -e "\e[0;31mUndefined $name\e[m"
		exit 1
	elif [ "$1" = "0" ] ; then
		echo -e "\e[0;31mIllegal $name\e[m"
		exit 1
	else
		echo "$name="$@
	fi
	return 0
}

function status()
{
	if [ "$2" = "0" ] ; then
		echo -e "\e[0;32m$1 Passed\e[m"
		return 0
	else
		echo -e "\e[0;31m$1 Failed\e[m"
		return 1
	fi
}

function i2c_set1()
{
local ibus chip data addr
local force=""
local autoy=""
local allow=""
local rback=""
local mask=""
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do
  case $1 in
    -h|--help)
    i2cset -h
    exit 1
    ;;
    -V)
    i2cset -V
    exit 1
    ;;
    -f)
    force="-f"
    ;;
    -y)
    autoy="-y"
    ;;
    -a)
    allow="-a"
    ;;
    -r)
    rback="-r"
    ;;
    -m)
    shift; mask="-m $(($1))"
    ;;
    *)
    #echo -e "\e[0;31mUndefined option $1\e[m"
    ;;
  esac
  shift
done
if [[ "$1" == '--' ]]; then shift; fi
test -n "$1" && ibus=$1 || try I2CBUS
shift
test -n "$1" && chip=$1 || try CHIP-ADDRESS
shift
test -n "$1" && addr=$1 || try DATA-ADDRESS
shift
test -n "$1" && data=$@ || try VALUE
i2cset $force $autoy $allow $rback $mask $ibus $chip $addr $data
return $?
}

function i2c_set2()
{
local ibus chip data amsb alsb
local force=""
local autoy=""
local allow=""
local rback=""
local mask=""
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do
  case $1 in
    -h|--help)
    i2cset -h
    exit 1
    ;;
    -V)
    i2cset -V
    exit 1
    ;;
    -f)
    force="-f"
    ;;
    -y)
    autoy="-y"
    ;;
    -a)
    allow="-a"
    ;;
    -r)
    rback="-r"
    ;;
    -m)
    shift; mask="-m $(($1))"
    ;;
    *)
    #echo -e "\e[0;31mUndefined option $1\e[m"
    ;;
  esac
  shift
done
if [[ "$1" == '--' ]]; then shift; fi
test -n "$1" && ibus=$1 || try I2CBUS
shift
test -n "$1" && chip=$1 || try CHIP-ADDRESS
shift
test -n "$1" && amsb=$1 || try DATA-ADDRESS
shift
test -n "$1" && alsb=$1 || try DATA-ADDRESS 0
shift
test -n "$1" && data=$@ || try VALUE
i2cset $force $autoy $allow $rback $mask $ibus $chip $amsb $alsb $data
return $?
}

function i2c_get1()
{
local ibus chip addr
local force=""
local autoy=""
local allow=""
local mode="b"
local dlen=32
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do
  case $1 in
    -h|--help)
    usage
    exit 1
    ;;
    -V)
    i2cget -V
    exit 1
    ;;
    -f)
    force="-f"
    ;;
    -y)
    autoy="-y"
    ;;
    -a)
    allow="-a"
    ;;
    *)
    #echo -e "\e[0;31mUndefined option $1\e[m"
    ;;
  esac
  shift
done
if [[ "$1" == '--' ]]; then shift; fi
test -n "$1" && ibus=$1 || try I2CBUS
shift
test -n "$1" && chip=$1 || try CHIP-ADDRESS
shift
test -n "$1" && addr=$1 || try DATA-ADDRESS
shift
test -n "$1" && mode=$1
shift
test -n "$1" && dlen=$(($1)) || dlen=0
test -n "$dlen" -a "$dlen" -gt "32" && dlen=32
test -n "$dlen" -a "$dlen" -lt "1" && dlen=0
test "$mode" = "i" -a "$dlen" -ne "0" && mode=$(echo $mode $dlen)
i2cget $force $autoy $allow $ibus $chip $addr $mode
}

function i2c_get2()
{
local ibus chip mode dlen amsb alsb
local force=""
local autoy=""
local allow=""
local mode="b"
local dlen="32"
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do
  case $1 in
    -h|--help)
    usage
    exit 1
    ;;
    -V)
    i2cget -V
    exit 1
    ;;
    -f)
    force="-f"
    ;;
    -y)
    autoy="-y"
    ;;
    -a)
    allow="-a"
    ;;
    -d)
    mode=$(($1))
    ;;
    -l)
    dlen=$(($1))
    ;;
    *)
    #echo -e "\e[0;31mUndefined option $1\e[m"
    ;;
  esac
  shift
done
if [[ "$1" == '--' ]]; then shift; fi
test -n "$1" && ibus=$1 || try I2CBUS
shift
test -n "$1" && chip=$1 || try CHIP-ADDRESS
shift
test -n "$1" && amsb=$1 || try DATA-ADDRESS
shift
test -n "$1" && alsb=$1 || try DATA-ADDRESS 0
shift
test -n "$1" && mode=$1
shift
test -n "$1" && dlen=$(($1)) || dlen=0
test -n "$dlen" -a "$dlen" -gt "32" && dlen=32
test -n "$dlen" -a "$dlen" -lt "1" && dlen=0
test "$mode" = "i" -a "$dlen" -ne "0" && mode=$(echo $mode $dlen)
i2cget $force $autoy $allow $ibus $chip $amsb $alsb $mode
}

function set_i2c_regb()
{
local target i2cbus devAdd regAdd regVal
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && regAdd="$1" || try DATA-ADDRESS
shift
test -n "$1" && regVal="$@" || try DATA-VALUE
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, Value $regVal"
i2c_set1 -f -y $i2cbus $devAdd $regAdd $regVal
return $?
}

function chk_i2c_regb()
{
local target i2cbus devAdd regAdd regVal hexVal mode
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && regAdd="$1" || try DATA-ADDRESS
shift
test -n "$1" && regVal="$@" || try DATA-VALUE
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd"
hexVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd b)
[[ "$hexVal" =~ ^0x ]] || { echo "i2cget: $hexVal"; try Value 0; }
echo "expected data: $regVal"
echo "received data: $hexVal"
test "$hexVal" = "$regVal"
#status "The comparison" $?
return $?
}

function chk_i2c_regw()
{
local target i2cbus devAdd regAdd regVal hexVal
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && regAdd="$1" || try DATA-ADDRESS
shift
test -n "$1" && regVal="$@" || try DATA-VALUE
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd"
hexVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd w)
[[ "$hexVal" =~ ^0x ]] || { echo "i2cget: $hexVal"; try Value 0; }
echo "expected data: $regVal"
echo "received data: $hexVal"
test "$hexVal" = "$regVal"
#status "The comparison" $?
return $?
}

function chk_i2c_tmp75b()
{
local target i2cbus devAdd regAdd minVal maxVal hexVal hex
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && regAdd="$1" || try DATA-ADDRESS
shift
test -n "$1" && minVal="$1" || try DATA-VALUE
shift
test -n "$1" && maxVal="$1" || try DATA-VALUE 0
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd"
hexVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd b)
[[ "$hexVal" =~ ^0x ]] || { echo "i2cget: $hexVal"; try Value 0; }
#echo "received data: $hexVal, expected greater than $minVal or less than $maxVal"
hex=$(($hexVal))
max=$(($maxVal))
min=$((-((~$minVal & 0x7f)+1)))
echo "received data: $hex, expected greater than $min and less than $max"
test "$hex" -gt "$min" -a "$hex" -lt "$max"
#status "The tolerance" $?
return $?
}

function chk_i2c_regs()
{
local target i2cbus devAdd regAdd regVal hexVal
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && regAdd="$1" || try DATA-ADDRESS
shift
test -n "$1" && regVal="$@" || try DATA-VALUE
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd"
#The Status register is first read to clear
hexVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd b)
[[ "$hexVal" =~ ^0x ]] || { echo "i2cget: $hexVal"; try Value 0; }
sleep 0.1
#The Status Register is read again for verification
hexVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd b)
[[ "$hexVal" =~ ^0x ]] || { echo "i2cget: $hexVal"; try Value 0; }
echo "expected data: $regVal"
echo "received data: $hexVal"
test "$hexVal" = "$regVal"
#status "The comparison" $?
return $?
}

function chk_i2c_exp_p0()
{
local target i2cbus devAdd regAdd cfgVal outVal inpVal
local polVal="0x00"
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
regAdd=0x04 #Polarity Inversion Port
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cset: $polVal"
i2c_set1 -f -y $i2cbus $devAdd $regAdd $polVal
regAdd=0x06 #Configuration Port
cfgVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd)
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cget: $cfgVal"
regAdd=0x02 #Output Port
outVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd)
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cget: $outVal"
outVal=$(($outVal&~$cfgVal))
regAdd=0x00 #Input Port
inpVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd)
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cget: $inpVal"
inpVal=$(($inpVal&~$cfgVal))
test "$inpVal" -eq "$outVal"
printf "$refdes port0: Expected 0x%02X \n" $outVal
printf "$refdes port0: Received 0x%02X \n" $inpVal
test "$inpVal" -eq "$outVal"
status "The comparison" $?
return $?
}

function chk_i2c_exp_p1()
{
local target i2cbus devAdd regAdd cfgVal outVal inpVal
local polVal="0x00"
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
regAdd=0x05 #Polarity Inversion Port
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cset: $polVal"
i2c_set1 -f -y $i2cbus $devAdd $regAdd $polVal
regAdd=0x07 #Configuration Port
cfgVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd)
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cget: $cfgVal"
regAdd=0x03 #Output Port
outVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd)
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cget: $outVal"
outVal=$(($outVal&~$cfgVal))
regAdd=0x01 #Input Port
inpVal=$(i2c_get1 -f -y $i2cbus $devAdd $regAdd)
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd $regAdd, i2cget: $inpVal"
inpVal=$(($inpVal&~$cfgVal))
printf "$refdes port1: Expected 0x%02X \n" $outVal
printf "$refdes port1: Received 0x%02X \n" $inpVal
test "$inpVal" -eq "$outVal"
status "The comparison" $?
return $?
}

function chk_i2c_eeprom()
{
which xxd > /dev/null || try xxd
which hexdump > /dev/null || try hexdump
which diff > /dev/null || try diff
f_in="/tmp/eesource.bin"
fout="/tmp/eetarget.bin"
local target i2cbus devAdd ret eeaddr eedata addr ad da dsize
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && eeaddr="$1" || try DATA-ADDRESS
shift
test -n "$1" && eedata="$@" || try DATA-VALUE
let ret=0
rm -f $f_in $fout
touch $f_in $fout
echo -e "$target i2c-$i2cbus, DevAdd $devAdd, Address $eeaddr, Write $eedata"
let addr=$devAdd
let ad=$eeaddr
for da in $(echo -e $eedata) ; do
test "$ad" -gt "0" -a "$((${ad}%256))" = "0" && {
    let addr++
    echo ADDRESS=$(printf %2x $addr)
}
ad=$((${ad}%256))
[[ "$da" =~ ^0x ]] || {
#try Value 0
echo "$da"
continue
}
#echo "i2cset -f -y $i2cbus $addr $ad $da b"
#i2cset -f -y $i2cbus $addr $ad $da b
i2c_set1 -f -y $i2cbus $addr $ad $da b
echo "$da" |xxd -r >> $f_in
let ret+=$?
sleep 0.01
let ad++
done
let addr=$devAdd
let dsize=$ad
let ad=$eeaddr
for ad in $(seq 0 1 $((dsize-1))); do
test "$ad" -gt "0" -a "$((${ad}%256))" = "0" && {
    let addr++
    echo ADDRESS=$(printf %2x $addr)
}
ad=$((${ad}%256))
#echo "i2cget -f -y $i2cbus $addr $ad"
#i2cget -f -y $i2cbus $addr $ad b |xxd -r >> $fout
i2c_get1 -f -y $i2cbus $addr $ad i 1 |xxd -r >> $fout
let ret+=$?
done
test -s "$f_in" || try infile 0
echo "expected data ($f_in):"
hexdump -Cv $f_in
echo -e "____________________________________________________________"
echo
test -s "$fout" || try outfile 0
echo "received data ($fout):"
hexdump -Cv $fout
echo -e "____________________________________________________________"
echo
diff -s $f_in $fout
let ret+=$?
#status "$target EEPROM Programming" $ret
return $ret
}

function tda_tps389008_dr_pri_b2_1()
{
local target i2cbus devAdd regArr mVolt mVminA mVmaxA mulArr hex channels errors
regArr=(7 0x40 0x41 0x42 0x43 0x44 0x45 0x46)
mulArr=(7 1 1 1 1 4 1 4)
mVminA=(7 750 750 1040 800 1710 750 1710)
mVmaxA=(7 850 850 1160 900 1890 850 1890)
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && channels="$@" || try Using_Channels
let errors=0
for ch in $channels; do
  hex=$(i2c_get1 -f -y $i2cbus $devAdd ${regArr[$ch]})
  echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd ${regArr[$ch]}, received data: $hex"
  [[ "$hex" =~ ^0x ]] || { echo "i2cget: $hex"; try Value 0; }
  mVolt=$((${mulArr[$ch]} * (200 + $hex * 5)))
  echo "$refdes MON$ch: $mVolt mV, expected between ${mVminA[$ch]} and ${mVmaxA[$ch]}"
  test "$mVolt" -ge "${mVminA[$ch]}" -a "$mVolt" -le "${mVmaxA[$ch]}"
  let errors+=$?
done
return $errors
}

function eth_tps389008_dr_pri_b2_1()
{
local target i2cbus devAdd regArr mVolt mVminA mVmaxA mulArr hex channels errors
regArr=(8 0x40 0x41 0x42 0x43 0x44 0x45 0x46 0x47)
mulArr=(8 1 1 1 1 1 1 4 4)
mVminA=(8 700 1100 700 1100 700 1100 1710 4750)
mVmaxA=(8 850 1260 850 1260 900 1260 1890 5250)
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && channels="$@" || try Using_Channels
let errors=0
for ch in $channels; do
  hex=$(i2c_get1 -f -y $i2cbus $devAdd ${regArr[$ch]})
  echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd ${regArr[$ch]}, received data: $hex"
  [[ "$hex" =~ ^0x ]] || { echo "i2cget: $hex"; try Value 0; }
  mVolt=$((${mulArr[$ch]} * (200 + $hex * 5)))
  echo "$refdes MON$ch: $mVolt mV, expected between ${mVminA[$ch]} and ${mVmaxA[$ch]}"
  test "$mVolt" -ge "${mVminA[$ch]}" -a "$mVolt" -le "${mVmaxA[$ch]}"
  let errors+=$?
done
return $errors
}

function com_tps389008_dr_pri_b2_1()
{
local target i2cbus devAdd regArr mVolt mVminA mVmaxA mulArr hex channels errors
regArr=(8 0x40 0x41 0x42 0x43 0x44 0x45 0x46 0x47)
mulArr=(8 1 4 1 1 1 4 1 4)
mVminA=(8 1030 4750 1140 1120 700 3130 1030 4750)
mVmaxA=(8 1150 5250 1260 1250 850 3470 1150 5250)
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && channels="$@" || try Using_Channels
let errors=0
for ch in $channels; do
  hex=$(i2c_get1 -f -y $i2cbus $devAdd ${regArr[$ch]})
  echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd ${regArr[$ch]}, received data: $hex"
  [[ "$hex" =~ ^0x ]] || { echo "i2cget: $hex"; try Value 0; }
  mVolt=$((${mulArr[$ch]} * (200 + $hex * 5)))
  echo "$refdes MON$ch: $mVolt mV, expected between ${mVminA[$ch]} and ${mVmaxA[$ch]}"
  test "$mVolt" -ge "${mVminA[$ch]}" -a "$mVolt" -le "${mVmaxA[$ch]}"
  let errors+=$?
done
return $errors
}

function eq1_tps389008_dr_pri_b2_1()
{
local target i2cbus devAdd regArr mVolt mVminA mVmaxA mulArr hex channels errors
regArr=(8 0x40 0x41 0x42 0x43 0x44 0x45 0x46 0x47)
mulArr=(8 1 4 4 1 1 1 1 4)
mVminA=(8 800 1710 1740 800 700 1000 450 1710)
mVmaxA=(8 900 1890 1860 900 800 1100 550 1890)
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && channels="$@" || try Using_Channels
let errors=0
for ch in $channels; do
  hex=$(i2c_get1 -f -y $i2cbus $devAdd ${regArr[$ch]})
  echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd ${regArr[$ch]}, received data: $hex"
  [[ "$hex" =~ ^0x ]] || { echo "i2cget: $hex"; try Value 0; }
  mVolt=$((${mulArr[$ch]} * (200 + $hex * 5)))
  echo "$refdes MON$ch: $mVolt mV, expected between ${mVminA[$ch]} and ${mVmaxA[$ch]}"
  test "$mVolt" -ge "${mVminA[$ch]}" -a "$mVolt" -le "${mVmaxA[$ch]}"
  let errors+=$?
done
return $errors
}

function eq0_tps389008_dr_pri_b2_1()
{
local target i2cbus devAdd regArr mVolt mVminA mVmaxA mulArr hex channels errors
regArr=(8 0x40 0x41 0x42 0x43 0x44 0x45 0x46 0x47)
mulArr=(8 1 4 4 1 1 1 1 4)
mVminA=(8 800 1710 1740 800 700 1000 450 1710)
mVmaxA=(8 900 1890 1860 900 800 1100 550 1890)
test -n "$1" && target="$1" || try DEVICE
shift
test -n "$1" && i2cbus="$1" || try I2CBUS
shift
test -n "$1" && devAdd="$1" || try CHIP-ADDRESS
shift
test -n "$1" && channels="$@" || try Using_Channels
let errors=0
for ch in $channels; do
  hex=$(i2c_get1 -f -y $i2cbus $devAdd ${regArr[$ch]})
  echo -e "$target i2c-$i2cbus, DevAdd $devAdd, RegAdd ${regArr[$ch]}, received data: $hex"
  [[ "$hex" =~ ^0x ]] || { echo "i2cget: $hex"; try Value 0; }
  mVolt=$((${mulArr[$ch]} * (200 + $hex * 5)))
  echo "$refdes MON$ch: $mVolt mV, expected between ${mVminA[$ch]} and ${mVmaxA[$ch]}"
  test "$mVolt" -ge "${mVminA[$ch]}" -a "$mVolt" -le "${mVmaxA[$ch]}"
  let errors+=$?
done
return $errors
}
