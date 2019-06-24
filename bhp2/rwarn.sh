#!/bin/bash
#for i in {1..4}; do echo $RANDOM; done
#n = $RANDOM
#echo "$n"
#echo $((RANDOM%180+60))
#n = $((RANDOM%180+60))
#od -vAn -N4 -tu4 < /dev/urandom
function rnum()
{
	num=$((RANDOM%40+15))
	#echo num
}
rnum
echo $num

notify-send "System is going down in $num minutes. Please save your work and log out" 
sudo shutdown -k $num 
sleep $num\m
bash $(pwd)/rwarn.sh
