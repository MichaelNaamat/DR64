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
exit $?
