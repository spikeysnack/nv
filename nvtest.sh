#!/bin/bash

# test the nv program 

echo "test nv"

NV=$(which nv)

[[ ! ${NV} ]] && NV="./nv"

[[ ! ${NV} ]] && NV="./nv.py"

[[ ! -f ${NV} ]] && echo "can't find nv -- install?" && exit


added=$( ${NV} 1 2 3 4 5)

echo "nv 1 2 3 4 5"
echo "${added}"
echo

pow2=$( ${NV} pow 2  1 2 3 4 5 6 7 8)
echo "nv pow 2 1 2 3 4 5 6 7 8"
echo "${pow2}"
echo

echo "nv \"pi * r**2\" # (r=2)"
r='2'
prsq=$( ${NV} "pi * ${r}**2" )
echo "${prsq}"
echo

echo "pipe test"
echo "echo \"1 2 3 4 5 5 6 7 8 9 10\" | nv mul"

mult=$(echo "1 2 3 4 5 6 7 8 9 10" | ${NV} mul)
echo "${mult}"
echo  


echo "file test"
f=$( ${NV} file read README.md)
echo "============================"
echo "${f}" | more

echo "============================"


