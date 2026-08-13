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
hexval="0x53"
test "$hexval" = "0x0" && hexval="0x00"
# read '0x53' from register '0x00' of 'U50' PF53 with address '0x28' at bus 'i2c-4'
refdes="U50"
i2cnum="4"
i2cdev="0x28"
offset="0x00"
chk_i2c_regb $refdes $i2cnum $i2cdev $offset $hexval
status "$refdes Register" $?
exit $?
