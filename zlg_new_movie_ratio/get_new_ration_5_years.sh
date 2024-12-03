#!/bin/bash

declare -a TEST
YEAR=($(ls 20*))
#echo ${TEST[0]}

for i in ${!YEAR[*]}
do
	if [ ${i} -eq 0 ]
	then
		exp_pat=" "
	elif [ ${i} -eq 1 ]
	then
		exp_pat=$(cat ${YEAR[0]}|tr '\n' '|' |sed 's#.$##g')
	elif [ ${i} -eq 2 ]
	then
		exp_pat=$(cat ${YEAR[0]} ${YEAR[1]}|tr '\n' '|' |sed 's#.$##g')
	elif [ ${i} -eq 3 ]
	then
		exp_pat=$(cat ${YEAR[0]} ${YEAR[1]} ${YEAR[2]} |tr '\n' '|' |sed 's#.$##g')
	elif [ ${i} -eq 4 ]
	then
		exp_pat=$(cat ${YEAR[0]} ${YEAR[1]} ${YEAR[2]} ${YEAR[3]}|tr '\n' '|' |sed 's#.$##g')
	else
		exp_pat=$(cat ${YEAR[i-5]} ${YEAR[i-4]} ${YEAR[i-3]} ${YEAR[i-2]} ${YEAR[i-1]}|tr '\n' '|' |sed 's#.$##g')
	fi
	new_num=$(cat ${YEAR[i]} |grep -Ewv "${exp_pat}" |wc -l)
	total_num=$(cat ${YEAR[i]} |wc -l)
	new_ratio=$(echo ${new_num} ${total_num} |awk '{printf "%d%" ,$1/$2*100}')
	echo ${YEAR[i]} ${new_num} ${total_num} ${new_ratio}
done
