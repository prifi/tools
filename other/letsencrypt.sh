#!/bin/bash
#

## Set Env
RemoteIp='172.22.0.208'
RemotePass=''
LogDate=$(date +%Y%m%d%H)
ScriptName=$(basename $0 .sh)
LogFile=/data/shell/logs/"$ScriptName".log."$LogDate"

## Log Setting
logInfo(){
   echo -e "\033[32m$(date "+%Y-%m-%d %T.%N") [INFO]:\t$1\033[0m"
}

## Reload Web1 Nginx
reloadNginx(){
    logInfo "Reload Web1 Nginx Start !!!" | tee -a $LogFile
    systemctl reload nginx | tee -a $LogFile
    logInfo "Reload Web1 Nginx Success !!!" | tee -a $LogFile
}

## Rsync Remote Web2
expectRsync(){
logInfo "Rsync letsencrypt Start !!!" | tee -a $LogFile
/usr/bin/expect -c"
set timeout 30;
spawn rsync -avzP /etc/letsencrypt/ $RemoteIp:/etc/letsencrypt/
expect {
\"*yes/no*\" {send \"yes\r\"; exp_continue}
\"*password*\" {send "\"$RemotePass"\r\";}
}
expect eof;" | tee -a $LogFile
logInfo "Rsync letsencrypt Success !!!" | tee -a $LogFile
}

expectReload(){
logInfo "Reload Web2 Nginx Start !!!" | tee -a $LogFile
/usr/bin/expect -c"
set timeout 30;
spawn ssh $RemoteIp systemctl reload nginx.service
expect {
\"*yes/no*\" {send \"yes\r\"; exp_continue}
\"*password*\" {send "\"$RemotePass"\r\";}
}
expect eof;" | tee -a $LogFile
logInfo "Reload Web2 Nginx Success !!!" | tee -a $LogFile
}

reloadNginx
expectRsync
expectReload

## Clear Old log
find /data/shell/logs -type f -name "$ScriptName.log.*" -mtime +30 -delete
