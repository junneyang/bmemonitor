#!/bin/sh

if [ $# != 1 ] ; then
	echo -e "ERROR : arguments missing"
	echo -e "Usage : ./start.sh <WorkNum>"
	exit 1; 
fi 

WorkNum=$1
i=0
while(($i<$WorkNum))
do
	nohup python gearWork.py > /dev/null 2>&1 &
	echo "work process "$i" started..."
	i=$(($i+1))
done
echo "all "$WorkNum" work process all started successfuly !"
