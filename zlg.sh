#!/bin/bash

token="S7fkezIl3Qd8ANapI2JBvh7EECcLr.T9rRDRacSDrQLCmQzDmQT9lgz5Uj0nkT8fbiMVXEdx.lgX7lAv6nQP9nwTAlwX6l.VczRlRqpe9jRoxqSYtXRlRqrfAr9mRq10VBqPbciSrQLRngr.VBq"

# movieId(showId) 
# showId(data-scheduleId)
MOVIE_INFO=(
'166430 777772579'
)

# multi_tickets 
# [{"id":"0000000029-10-24","name":"10排6座"},{"id":"0000000029-10-25","name":"10排8座"}]

FILM=(
'{"id":"00000000029-9-20","name":"9排3座"}'
'{"id":"00000000029-9-18","name":"9排7座"}'
'{"id":"00000000029-8-25","name":"8排8座"}'
'{"id":"00000000029-9-24","name":"9排6座"}'
'{"id":"00000000029-9-25","name":"9排8座"}'
)


max=5000
cout=0

while [ ${cout} -le ${max} ]
do

	for i in "${MOVIE_INFO[@]}"
	do
		movieId_and_showId=($i)
		movieId=${movieId_and_showId[0]}
		showId=${movieId_and_showId[1]}
		for i in ${FILM[@]}
		do
		        ts=$(date +%s |awk '{print $0"000"}')
			DATE=$(date +%Y%m%d)
			if [ $(curl -s "https://ticket.nexttix.net/api/orders?offset=0&limit=100&_token=${token}&_=${ts}"  |jq -r ".data |.list[] | select(.movieId == $movieId) |.orderNo" 2>/dev/null |grep -E "${DATE}" |wc -l) -ge 1 ]
			then
				echo "${movieId} has been bought before"	
				break
			fi
		        echo '['${i}']'
		        result=$(curl -s -X POST \
		          https://ticket.nexttix.net/api/shows/${showId}/lock \
		          -H "authorization: ${token}" \
		          -H 'accept: */*' \
		          -H 'accept-encoding: gzip, deflate, br' \
		          -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' \
		          -H 'cache-control: no-cache' \
		          -H 'content-type: application/json' \
		          -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' \
		          -d "[${i}]")
			[ $(echo ${result} |jq -r '.ret') -eq 4010 ] && echo "Invalid Token, exit" && exit 0
			if [ $(echo ${result} |jq -r '.ret') -eq 0 ]
			then
				break
			fi
			echo ${result}
			sleep 0.05
		done
	done
    	sleep 0.5
        ((++cout))
done

exit 0


curl -X POST \
  https://ticket.nexttix.net/api/shows/771807303/lock \
  -H "authorization: BdoENTDkBuQOiuBRfZj1HaiMUQg-1JU8DD.T9rRDRacSDrQLCmQzDmwPAnAX8Uj0lV4FsGEJ.lgX7lAv6nQP9nwTAlwX6l.VczRlRqpe9jRoxqSYtXRlRqrfAr9mRq10VBqPbciSrQLRngr.VBq" \
  -H 'accept: */*' \
  -H 'accept-encoding: gzip, deflate, br' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' \
  -d "[{"id":"000000000029-2-4","name":"2排32座"}]"
