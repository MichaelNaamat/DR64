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

refdes="U146"
i2cnum="0"
i2cdev="0x74"
let sta=0
chk_i2c_exp_p0 $refdes $i2cnum $i2cdev
let sta+=$?
chk_i2c_exp_p1 $refdes $i2cnum $i2cdev
let sta+=$?
status "$refdes Register Values" $sta
exit $sta
