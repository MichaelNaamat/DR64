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

let sta=0
# write to 'U127' with address '0x49' at bus 'i2c-0'
refdes="U127"
i2cnum="0"
i2cdev="0x49"
test -n "$1" && TloVal="$1" || \
TloVal="0xd8"
# write '0xd8 0x00' to register '0x02'
offset="0x02"
set_i2c_regb $refdes $i2cnum $i2cdev $offset $TloVal 0x00 i
status "$refdes Temperature Low Limit Register" $?
let sta+=$?
shift
test -n "$1" && ThiVal="$1" || \
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
exit $?
