#!/bin/bash

. .env

TMPISO="/tmp/$ISOFILE"

cp -f $ISO $TMPISO

virt-install --connect qemu:///system --virt-type kvm --name ${VMNAME} --description '${DESCRIPTION}' --os-variant=${OSVARIANT} --ram=${RAM} --vcpus=${VCPUS} --disk path=${DISK},size=${SIZE} -l ${TMPISO} --initrd-inject="./preseed.cfg" --extra-args="preseed/file=/preseed.cfg"
