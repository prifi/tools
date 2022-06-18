#!/usr/bin/env bash
set -u

trap 'rm -f "$TMPFILE"' EXIT
TMPFILE=$(mktemp) || exit 1

flag=0
UP_TOTAL=$(du -sh dest |awk 'NR==3 {printf ("%.2f%s\n",$3/1024/1024/1024,"G")}')

upload() {
   cp -r src/ dest/ > /dev/null 2>&1
  if [[ "$?" -ne 0 ]]; then
    let flag+=1
  fi
}

upload
if [[ $flag -ne 0 ]];then
  MESSAGE="<font color=\\\"warning\\\">[Cron-10.1.1.22] 备份失败，上次备份大小：${UP_TOTAL}</font>\n"
else
  CUR_TOTAL=$(/bin/ossutil64 du oss://supplychain-prod-image/ |awk 'NR==3 {printf ("%.2f%s\n",$3/1024/1024/1024,"G")}')
  MESSAGE="<font color=\\\"info\\\">[Cron-10.1.1.22] 备份成功，上次备份：${UP_TOTAL}，当前：${CUR_TOTAL} </font>\n"
fi

echo "{" >${TMPFILE}
echo "  \"msgtype\": \"markdown\"," >>${TMPFILE}
echo "  \"markdown\": {" >>${TMPFILE}
echo "    \"content\": \"${MESSAGE}\"" >>${TMPFILE}
echo "  }" >>${TMPFILE}
echo "}" >>${TMPFILE}

curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx' -H 'Content-Type: application/json' -d @${TMPFILE}