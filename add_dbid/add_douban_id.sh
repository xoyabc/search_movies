#!/bin/bash

cp sample.json result.json

cat dbid_info |sed 's#"##g' |awk -F "[\t ]+" '{print $1}' |sort -u |while read NAME
do
    #NAME=$(echo ${line} |sed 's#"##g' |awk -F "\t" '{print $1}')
    DB_ID=$(cat dbid_info |grep "${NAME}" |sed 's#"##g' |awk -F "\t" '{print $2}' |head -n 1)
    echo ${DB_ID}
    DB_ID_INFO='"dbid": "'${DB_ID}'",'
    echo ${DB_ID_INFO}
    #sed -r '/姑娘/i\ \ \ \ \ \ \ \ "dbid": "6785697",' a.json > 3
    #sed -ri "/\"${NAME}\"/i\ \ \ \ \ \ \ \ ${DB_ID_INFO}" result.json
    sed -ri "/\"${NAME}\"/i${DB_ID_INFO}" result.json
done
