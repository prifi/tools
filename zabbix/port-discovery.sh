#!/bin/bash 
#mysql low-level discovery 
res=$(netstat -lntp|awk -F "[ :\t]+" '/docker/{print$4}' |grep -v "0.0.0.0")
port=($res)
printf '{' 
printf '"data":[' 
for key in ${!port[@]} 
do 
        if [[ "${#port[@]}" -gt 1 && "${key}" -ne "$((${#port[@]}-1))" ]];then 
                printf '{' 
                printf "\"{#MYSQLPORT}\":\"${port[${key}]}\"}," 
        else [[ "${key}" -eq "((${#port[@]}-1))" ]] 
                printf '{' 
                printf "\"{#MYSQLPORT}\":\"${port[${key}]}\"}" 
        fi 
done 
printf ']' 
printf '}\n'