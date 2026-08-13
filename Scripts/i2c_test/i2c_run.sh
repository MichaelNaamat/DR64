#!/bin/bash

function put_header()
{
echo -e "$0 $@"
echo -e "____________________________________________________________"
echo -e ""
}

test -z "$(echo $PATH |grep "$PWD:")" && export PATH=$PWD:$PATH
name=i2c_lib.sh
lib=$(which $name)
test ! -z "$lib" || { 
echo -e "\e[0;31mUndefined $name\e[m"
exit 1
}
test -s "$lib" || {
echo -e "\e[0;31mIllegal $name\e[m"
exit 1
}
source $lib
put_header $@

function A_U100()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'A_U100' with address '0x46' at bus 'i2c-1'
refdes="A_U100"
i2cnum="1"
i2cdev="0x46"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function A_U18()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'A_U18' with address '0x43' at bus 'i2c-1'
refdes="A_U18"
i2cnum="1"
i2cdev="0x43"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function A_U26()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'A_U26' with address '0x40' at bus 'i2c-1'
refdes="A_U26"
i2cnum="1"
i2cdev="0x40"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function B_U100()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'B_U100' with address '0x46' at bus 'i2c-2'
refdes="B_U100"
i2cnum="2"
i2cdev="0x46"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function B_U18()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'B_U18' with address '0x43' at bus 'i2c-2'
refdes="B_U18"
i2cnum="2"
i2cdev="0x43"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function B_U26()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'B_U26' with address '0x40' at bus 'i2c-2'
refdes="B_U26"
i2cnum="2"
i2cdev="0x40"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function U103()
{
refdes="U103"
i2cnum="4"
i2cdev="0x74"
let sta=0
chk_i2c_exp_p0 $refdes $i2cnum $i2cdev
let sta+=$?
chk_i2c_exp_p1 $refdes $i2cnum $i2cdev
let sta+=$?
status "$refdes Register Values" $sta
return $?
}

function U104()
{
refdes="U104"
i2cnum="0"
i2cdev="0x75"
let sta=0
chk_i2c_exp_p0 $refdes $i2cnum $i2cdev
let sta+=$?
chk_i2c_exp_p1 $refdes $i2cnum $i2cdev
let sta+=$?
status "$refdes Register Values" $sta
return $?
}

function U114()
{
testVM="1 2 3 4 5 6 7 8"
refdes="U114"
i2cnum="0"
i2cdev="0x34"
eth_tps389008_dr_pri_b2_1 $refdes $i2cnum $i2cdev $testVM
status "$refdes ADC_MON Registers" $?
return $?
}

function U127()
{
let sta=0
# write to 'U127' with address '0x49' at bus 'i2c-0'
refdes="U127"
i2cnum="0"
i2cdev="0x49"
#test -n "$1" && TloVal="$1" || \
TloVal="0xd8"
# write '0xd8 0x00' to register '0x02'
offset="0x02"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $TloVal 0x00 i
status "$refdes Temperature Low Limit Register" $?
let sta+=$?
shift
#test -n "$1" && ThiVal="$1" || \
ThiVal="0x69"
# write '0x69 0x00' to register '0x03'
offset="0x03"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $ThiVal 0x00 i
status "$refdes Temperature High Limit Register" $?
let sta+=$?
# read value from register '0x00'
offset="0x00"
# check that the reading value is greater than or equal to $TloVal and less than or equal to $ThiVal
chk_i2c_tmp75b $refdes $i2cnum $i2cdev $offset $TloVal $ThiVal
let sta+=$?
status "$refdes Temperature Register Value" $sta
return $?
}

function U146()
{
refdes="U146"
i2cnum="0"
i2cdev="0x74"
let sta=0
chk_i2c_exp_p0 $refdes $i2cnum $i2cdev
let sta+=$?
chk_i2c_exp_p1 $refdes $i2cnum $i2cdev
let sta+=$?
status "$refdes Register Values" $sta
return $?
}

function U148()
{
testVM="1 2 3 4 5 6 7"
refdes="U148"
i2cnum="4"
i2cdev="0x34"
tda_tps389008_dr_pri_b2_1 $refdes $i2cnum $i2cdev $testVM
status "$refdes ADC_MON Registers" $?
return $?
}

function U32()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'U32' with address '0x30' at bus 'i2c-2'
refdes="U32"
i2cnum="2"
i2cdev="0x30"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function U33()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'U33' with address '0x33' at bus 'i2c-1'
refdes="U33"
i2cnum="1"
i2cdev="0x33"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function U34()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'U34' with address '0x43' at bus 'i2c-2'
refdes="U34"
i2cnum="2"
i2cdev="0x43"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
return $?
}

function U50()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x53"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x53' from register '0x00' of 'U50' PF53 with address '0x28' at bus 'i2c-4'
refdes="U50"
i2cnum="4"
i2cdev="0x28"
offset="0x00"
chk_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Register" $?
return $?
}

function U54()
{
local hexval
let sta=0
#test -n "$1" && hexval="$1" || \
hexval="0x6121"
test "$hexval" = "0x0" && hexval="0x0000"
# read '0x6121' from register '0x2b' of 'U54' with address '0x20' at bus 'i2c-4'
refdes="U54"
i2cnum="4"
i2cdev="0x20"
offset="0x2b"
chk_i2c_regw $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes M_DEVICEID Register" $?
let sta+=$?
#shift
#test -n "$1" && hexval="$1" || \
hexval="0x0f06"
test "$hexval" = "0x0" && hexval="0x0000"
# read '0x0f06' from register '0x16' of 'U54' with address '0x21' at bus 'i2c-4'
refdes="U54"
i2cnum="4"
i2cdev="0x21"
offset="0x16"
chk_i2c_regw $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes FS_DIAG_SAFETY Register" $?
let sta+=$?
return $sta
}

function U59()
{
local hexval
echo -e "I2C EEPROM Test"
echo -e "____________________________________________________________"
echo -e ""
test -n "$1" && hexval="$@" || \
hexval="0x60 0x00 0x00 0x00"
test "$hexval" = "0x0" && hexval="0x00"
# write "0x60 0x00 0x00 0x00" to EEPROM 'U59' with address '0x50' at bus 'i2c-0'
refdes="U59"
i2cnum="0"
i2cdev="0x50"
offset="0x00"
chk_i2c_eeprom $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes EEPROM Programming" $?
return $?
}

function U60()
{
let sta=0
# write to 'U60' with address '0x48' at bus 'i2c-4'
refdes="U60"
i2cnum="4"
i2cdev="0x48"
#test -n "$1" && TloVal="$1" || \
TloVal="0xd8"
# write '0xd8 0x00' to register '0x02'
offset="0x02"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $TloVal 0x00 i
status "$refdes Temperature Low Limit Register" $?
let sta+=$?
#shift
#test -n "$1" && ThiVal="$1" || \
ThiVal="0x69"
# write '0x69 0x00' to register '0x03'
offset="0x03"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $ThiVal 0x00 i
status "$refdes Temperature High Limit Register" $?
let sta+=$?
# read value from register '0x00'
offset="0x00"
# check that the reading value is greater than or equal to $TloVal and less than or equal to $ThiVal
chk_i2c_tmp75b $refdes $i2cnum $i2cdev $offset $TloVal $ThiVal
let sta+=$?
status "$refdes Temperature Register Value" $sta
return $?
}

function U61()
{
let sta=0
# write to 'U61' with address '0x4c' at bus 'i2c-4'
refdes="U61"
i2cnum="4"
i2cdev="0x4c"
#test -n "$1" && TloVal="$1" || \
TloVal="0xd8"
# write '0xd8 0x00' to register '0x02'
offset="0x02"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $TloVal 0x00 i
status "$refdes Temperature Low Limit Register" $?
let sta+=$?
#shift
#test -n "$1" && ThiVal="$1" || \
ThiVal="0x69"
# write '0x69 0x00' to register '0x03'
offset="0x03"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $ThiVal 0x00 i
status "$refdes Temperature High Limit Register" $?
let sta+=$?
# read value from register '0x00'
offset="0x00"
# check that the reading value is greater than or equal to $TloVal and less than or equal to $ThiVal
chk_i2c_tmp75b $refdes $i2cnum $i2cdev $offset $TloVal $ThiVal
let sta+=$?
status "$refdes Temperature Register Value" $sta
return $?
}

function U62()
{
let sta=0
# write to 'U62' with address '0x49' at bus 'i2c-4'
refdes="U62"
i2cnum="4"
i2cdev="0x49"
#test -n "$1" && TloVal="$1" || \
TloVal="0xd8"
# write '0xd8 0x00' to register '0x02'
offset="0x02"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $TloVal 0x00 i
status "$refdes Temperature Low Limit Register" $?
let sta+=$?
#shift
#test -n "$1" && ThiVal="$1" || \
ThiVal="0x69"
# write '0x69 0x00' to register '0x03'
offset="0x03"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $ThiVal 0x00 i
status "$refdes Temperature High Limit Register" $?
let sta+=$?
# read value from register '0x00'
offset="0x00"
# check that the reading value is greater than or equal to $TloVal and less than or equal to $ThiVal
chk_i2c_tmp75b $refdes $i2cnum $i2cdev $offset $TloVal $ThiVal
let sta+=$?
status "$refdes Temperature Register Value" $sta
return $?
}

function U64()
{
let sta=0
# write to 'U64' with address '0x4a' at bus 'i2c-4'
refdes="U64"
i2cnum="4"
i2cdev="0x4a"
#test -n "$1" && TloVal="$1" || \
TloVal="0xd8"
# write '0xd8 0x00' to register '0x02'
offset="0x02"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $TloVal 0x00 i
status "$refdes Temperature Low Limit Register" $?
let sta+=$?
#shift
#test -n "$1" && ThiVal="$1" || \
ThiVal="0x69"
# write '0x69 0x00' to register '0x03'
offset="0x03"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $ThiVal 0x00 i
status "$refdes Temperature High Limit Register" $?
let sta+=$?
# read value from register '0x00'
offset="0x00"
# check that the reading value is greater than or equal to $TloVal and less than or equal to $ThiVal
chk_i2c_tmp75b $refdes $i2cnum $i2cdev $offset $TloVal $ThiVal
let sta+=$?
status "$refdes Temperature Register Value" $sta
return $?
}

function U87()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x6a"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x6a' from register '0x21' of 'U87' with address '0x6a' at bus 'i2c-1'
refdes="U87"
i2cnum="1"
i2cdev="0x6a"
offset="0x21"
chk_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes I2C_ADDR Register" $?
return $?
}

function U88()
{
local hexval
#test -n "$1" && hexval="$1" || \
hexval="0x6a"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x6a' from register '0x21' of 'U87' with address '0x6a' at bus 'i2c-1'
refdes="U88"
i2cnum="1"
i2cdev="0x6b"
offset="0x21"
chk_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes I2C_ADDR Register" $?
return $?
}

function U93()
{
testVM="1 2 3 4 5 6 7 8"
refdes="U93"
i2cnum="0"
i2cdev="0x37"
eq0_tps389008_dr_pri_b2_1 $refdes $i2cnum $i2cdev $testVM
status "$refdes ADC_MON Registers" $?
return $?
}

function U94()
{
testVM="1 2 3 4 5 6 7 8"
refdes="U94"
i2cnum="0"
i2cdev="0x36"
eq1_tps389008_dr_pri_b2_1 $refdes $i2cnum $i2cdev $testVM
status "$refdes ADC_MON Registers" $?
return $?
}

function U95()
{
testVM="1 2 3 4 5 6 7 8"
refdes="U95"
i2cnum="0"
i2cdev="0x35"
com_tps389008_dr_pri_b2_1 $refdes $i2cnum $i2cdev $testVM
status "$refdes ADC_MON Registers" $?
return $?
}

function EQ0_Vddq()
{
local hexval
test -n "$1" && hexval="$1" || \
hexval="0x14"
# write '0x14' for 0.5V or write '0x50' for 0.8V
test "$hexval" = "0x0" && hexval="0x00"
# write to register '0x00' of 'A_U26' with address '0x40' at bus 'i2c-1'
refdes="A_U26"
i2cnum="1"
i2cdev="0x40"
offset="0x00"
let sta=0
set_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
let sta+=$?
chk_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
let sta+=$?
status "$refdes Configurarion" $sta
return $?
}

function EQ1_Vddq()
{
local hexval
test -n "$1" && hexval="$1" || \
hexval="0x14"
# write '0x14' for 0.5V or write '0x50' for 0.8V
test "$hexval" = "0x0" && hexval="0x00"
# write to register '0x00' of 'B_U26' with address '0x40' at bus 'i2c-2'
refdes="B_U26"
i2cnum="2"
i2cdev="0x40"
offset="0x00"
let sta=0
set_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
let sta+=$?
chk_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
let sta+=$?
status "$refdes Configurarion" $sta
return $?
}

function select_list()
{
LIST=$(echo "one clock prom gpio temp vmon vreg vddq all")
case $1 in
	-o|--one|/one|1)
		list="one"
		shift
		;;
	-c|--clock|/clock|2)
		list="clock"
		shift
		;;
	-p|--prom|/prom|3)
		list="prom"
		shift
		;;
	-g|--gpio|/gpio|4)
		list="gpio"
		shift
		;;
	-t|--temp|/temp|5)
		list="temp"
		shift
		;;
	-m|--vmon|/vmon|6)
		list="vmon"
		shift
		;;
	-r|--vreg|/vreg|7)
		list="vreg"
		shift
		;;
	-d|--vddq|/vddq|8)
		list="vddq"
		shift
		;;
	-a|--all|/all|9)
		list="all"
		shift
		;;
	*)
		echo "Select List:"
		select list in $LIST ; do
			list=$list
			break
		done
		;;
esac
try List $list
select_refdes $list $@
return $?
}

function select_refdes()
{
REFDES2=$(echo "U87 U88")
REFDES3=$(echo "U59")
REFDES4=$(echo "U103 U104 U146")
REFDES5=$(echo "U127 U60 U61 U62 U64")
REFDES6=$(echo "U114 U93 U94 U95") #U148 Not_in_BOM
REFDES7=$(echo "A_U100 A_U18 A_U26 B_U100 B_U26 U32 U33 U34 U50 U54") #B_U18 NA
REFDES8=$(echo "EQ0_Vddq EQ1_Vddq")
REFDES9=$(echo "$REFDES2 $REFDES4 $REFDES5 $REFDES6 $REFDES7 $REFDES8 $REFDES3")
case $1 in 
	one|1)
		shift
		refdes="$1"
		test -z "$refdes" && {
			echo "Select Ref_Des:"
			select refdes in $REFDES9 ; do
				refdes=$refdes
				break
			done
		} || shift
		;;
	clock|2)
		refdes="$REFDES2"
		shift
		;;
	prom|3)
		refdes="$REFDES3"
		shift
		;;
	gpio|4)
		refdes="$REFDES4"
		shift
		;;
	temp|5)
		refdes="$REFDES5"
		shift
		;;
	vmon|6)
		refdes="$REFDES6"
		shift
		;;
	vreg|7)
		refdes="$REFDES7"
		shift
		;;
	vddq|8)
		refdes="$REFDES8"
		shift
		;;
	all|9)
		refdes="$REFDES9"
		shift
		;;
	*)
		echo "Select Ref_Des:"
		select refdes in $REFDES9 ; do
			refdes=$refdes
			break
		done
		;;
esac
try RefDes $refdes
let sta=0
for name in $refdes; do
	#echo -e "____________________________________________________________"
	#echo -e ""
	#echo -e "$name $@"
	#echo -e "____________________________________________________________"
	#echo -e ""
	if [ "$list" = "one" -o "$list" = "prom" -o "$list" = "vddq" ] ; then
	    ./$name.sh $@
		#$name $@
	else
	    ./$name.sh
		#$name
	fi
	let sta+=$?
	#echo status=$sta
done
return $sta
}

select_list $@
status "I2C Test" $?
exit $?
