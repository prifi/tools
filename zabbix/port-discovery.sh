#!/usr/bin/env bash
#

res=$(sudo netstat -tnlp |awk -F"[ :]+" '/^tcp/ {print $4}' |grep -Ev "0.0.0.0|127.0.0.1|111|1")
port=($res)
printf '{'
printf '"data":['

for key in ${!port[@]}
do
  if [[ $key -ne $(( ${#port[@]}-1 )) ]];then
    printf "{\"{#PORT}\":\"%s\"}," ${port[$key]}
  else
    printf "{\"{#PORT}\":\"%s\"}" ${port[$key]}
  fi
done

printf ']'
printf '}\n'