#!/bin/bash
#This code belongs to HUNTER CARBONE
echo "THIS CODE IS PROPERTY OF HUNTER CARBONE"
echo "running check now"
if [[ $(md5sum $1 $2 | awk '{print $1}' | uniq | wc -l) == 1 ]]
then
    echo "Identical files"
else
    echo "There are differences"
fi
