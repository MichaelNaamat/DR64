#!/bin/bash

put_header()
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

testVM="1 2 3 4 5 6 7 8"

refdes="U94"
i2cnum="0"
i2cdev="0x36"
eq1_tps389008_dr_pri_b2_1 $refdes $i2cnum $i2cdev $testVM
status "$refdes ADC_MON Registers" $?
exit $?
