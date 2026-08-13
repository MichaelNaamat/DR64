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

let stats=0
test -n "$1" && hexval="$1" || \
hexval="0x6121"
test "$hexval" = "0x0" && hexval="0x0000"
# read '0x6121' from register '0x2b' of 'U54' with address '0x20' at bus 'i2c-4'
refdes="U54"
i2cnum="4"
i2cdev="0x20"
offset="0x2b"
chk_i2c_regw $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes M_DEVICEID Register" $?
let stats+=$?

shift
test -n "$1" && hexval="$1" || \
hexval="0x0f06"
test "$hexval" = "0x0" && hexval="0x0000"
# read '0x0f06' from register '0x16' of 'U54' with address '0x21' at bus 'i2c-4'
refdes="U54"
i2cnum="4"
i2cdev="0x21"
offset="0x16"
chk_i2c_regw $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes FS_DIAG_SAFETY Register" $?
let stats+=$?
exit $stats
