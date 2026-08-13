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
exit $?
