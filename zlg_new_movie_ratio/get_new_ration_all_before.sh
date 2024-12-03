#!/bin/bash

declare -a TEST
YEAR=($(ls 20*))
#echo ${TEST[0]}

for i in ${!YEAR[*]}
do
	year=${YEAR[i]} 
	exp_pat=$(cat 1.txt |awk -v thshold=${year} '$1<thshold{print $2}' |sort -u |tr '\n' '|' |sed 's#.$##g')
	#echo ${exp_pat}
	new_num=$(cat 1.txt |awk -v thshold=${year} '$1==thshold{print $2}' |grep -Ewv "${exp_pat}" |wc -l)
	total_num=$(cat 1.txt |awk -v thshold=${year} '$1==thshold{print $2}' |wc -l)
	new_ratio=$(echo ${new_num} ${total_num} |awk '{printf "%d%" ,$1/$2*100}')
	echo ${year} ${new_num} ${total_num} ${new_ratio}
done
