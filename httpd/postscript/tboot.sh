#!/bin/bash

PXE_SERVER=192.168.1.1
bootroot=/boot

wget -O $bootroot/tboot.gz http://$PXE_SERVER/postscript/tboot.gz
wget -O $bootroot/sinit.bin http://$PXE_SERVER/postscript/sinit.bin

num=`sed -n "/boot\/vmlinuz/=" /boot/grub/grub.cfg`
arr=($num)
first=${arr[0]}
num=`sed -n "/boot\/initrd\.img/=" /boot/grub/grub.cfg`
arr=($num)
sec=${arr[0]}
((sec++))
#sed -i "$first i hello world" /boot/grub/grub.cfg
#echo $first $sec
sed -i "$first i multiboot \/boot\/tboot.gz \/boot\/tboot.gz logging=serial,vga,memory" /boot/grub/grub.cfg
sed -i "$sec a module  \/boot\/sinit.bin \/boot\/sinit.bin" /boot/grub/grub.cfg
((first++))
sed -i "$first s/linux/module/" /boot/grub/grub.cfg
sed -i "$sec s/initrd/module/" /boot/grub/grub.cfg
