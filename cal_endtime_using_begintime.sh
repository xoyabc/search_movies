#!/bin/bash

cat begintime_duration |sed '/^\s*$/d' |while read line
do
        #start_time="14:30"
        #duration_min="150"
        start_time=$(echo ${line} |awk '{print $1}')
        duration_min=$(echo ${line} |awk '{print $2}')
        duration_sec=$(echo $((60*${duration_min})))
        #echo ${duration_sec}

        start_ts=$(date +%s --date "1995-12-28 ${start_time}")
        end_ts=$(echo $((${start_ts}+${duration_sec})))
        #echo ${end_ts}
        end_time=$(date +%H:%M -d @${end_ts})
        #echo "${start_time} ${duration_min} ${end_time} ${start_time}-${end_time}"
        printf "%-5s %3s %5s %11s\n" ${start_time} ${duration_min} ${end_time} ${start_time}-${end_time}
done
