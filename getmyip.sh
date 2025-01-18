#!/bin/bash
DEVC="${1:-tun0}"

IP=`ip a s $DEVC 2>&1`

if grep -q 'not' <<< "$IP"; then
  exit 1
else
    ip a s $DEVC | grep $DEVC | grep inet | awk -F " " '{ print $2 }' | sed 's/\/.*//'
    exit 0
fi


