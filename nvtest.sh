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

echo "nv 5 6 7 8 9"
nv 5 6 7 8 9

echo "nv max  13 45 6 7 8 22 31 41 7"
nv max  13 45 6 7 8 22 31 41 7
echo  

echo "nv pow 11 12"
nv pow 11 12 
echo  

echo "nv \"sin(pi/4) * 4\""
nv "sin(pi/4) * 4"
echo  

echo "nv runtimes 10 \"echo this line repeats 10 times.\""
nv runtimes 10 "echo This line repeats 10 times"

echo "============================"
read -p "Press enter to continue"

echo "pipe test"
echo "echo \"1 2 3 4 5 5 6 7 8 9 10\" | nv mul"
mult=$(echo "1 2 3 4 5 6 7 8 9 10" | ${NV} mul)
echo "${mult}"
echo  

echo "\"2 4 8 16 32 35\" | nv log10"
echo "2 4 8 16 32 35" | nv log10
echo  

echo "\"2 4 8 16 32 35\" | nv log2"
echo "2 4 8 16 32 35" | nv log2
echo  


echo "\"5 7 9 2 3\" | nv fdiv"
echo "5 7 9 2 3" | nv fdiv
echo  

echo "\"sin(pi/4\)\" | nv"
echo "sin(pi/4)" | nv
echo  

echo "============================"

read -p "Press enter to continue"

echo "file test -- nvtest.sh"
echo

f=$( ${NV} file read nvtest.sh)
echo "============================"
echo "${f}" | more
echo "============================"



