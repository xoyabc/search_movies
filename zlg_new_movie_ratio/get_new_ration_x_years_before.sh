#!/bin/bash

declare -a TEST
YEAR=($(ls 20*))
#echo ${TEST[0]}
YEAR_AGO=${1:-3}
echo ${YEAR_AGO}

for i in ${!YEAR[*]}
do
	year=${YEAR[i]} 
	year_start=$((${year}-${YEAR_AGO}))
	# exp_file
	cat 1.txt |awk -v thshold=${year} -v thshold_start=${year_start} '$1<thshold && $1>=thshold_start{print $2}' > tmp
	#echo ${exp_pat}
	new_num=$(cat 1.txt |awk -v thshold=${year} '$1==thshold{print $2}' |grep -Evf tmp |wc -l)
	total_num=$(cat 1.txt |awk -v thshold=${year} '$1==thshold{print $2}' |wc -l)
	new_ratio=$(echo ${new_num} ${total_num} |awk '{printf "%d%" ,$1/$2*100}')
	echo ${year} ${new_num} ${total_num} ${new_ratio}
done
