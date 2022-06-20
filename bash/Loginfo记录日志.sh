#!/bin/bash
#
set -eu
name=`basename $0 .sh`
logDate=$(date +%Y-%m)
logFile=/data/shell/logs/$name-$logDate.log
logInfo() {
    echo -e "\033[32m`date +'%F %H:%M:%S'`\t$1\033[0m" | tee -a $logFile
}

logInfo "Start!!!"
echo "---- xxx ----" | tee -a $logFile
logInfo "Done!!!"
