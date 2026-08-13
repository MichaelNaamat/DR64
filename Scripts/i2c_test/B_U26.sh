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

test -n "$1" && hexval="$1" || \
hexval="0x00"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x00' from the status register '0x04' of 'B_U26' with address '0x40' at bus 'i2c-2'
refdes="B_U26"
i2cnum="2"
i2cdev="0x40"
offset="0x04"
chk_i2c_regs $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Status Register" $?
exit $?
