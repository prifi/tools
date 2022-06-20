#!/usr/bin/env bash
set -euo pipefail
# Describe: Monotor slow url auto send. -- 20201206

trap 'rm -f "$TMPFILE"' EXIT
TMPFILE=$(mktemp) || exit 1

# base info
NGX_HOME="/data/service/nginx"
DOMAIN=$(hostname | sed -r 's/(.*)-(.*)-(.*)/\2/')
LOG_FILE="${NGX_HOME}/logs/${DOMAIN}.com_proxy_443_access.log"
C_DATE=$(date +'%d/%b/%Y')

five_txt="/root/shell_script/$(basename $0 .sh)/five.txt"
ten_txt="/root/shell_script/$(basename $0 .sh)/ten.txt"

cat ${LOG_FILE} | grep "${C_DATE}" | awk -F'\"' '$10>5' | awk -F"[ \"]" '{print $7,$8}' | awk -F"['?']" '{a[$1]++}END{for (i in a) print a[i],i}' | awk '$1>=10' | sort -nr > ${five_txt}
cat ${LOG_FILE} | grep "${C_DATE}" | awk -F'\"' '$10>10' | awk -F"[ \"]" '{print $7,$8}' | awk -F"['?']" '{a[$1]++}END{for (i in a) print a[i],i}' | awk '$1>=10' | sort -nr > ${ten_txt}
#cat ${LOG_FILE} | grep "${C_DATE}" | awk -F'\"' '$10>5' | awk -F"[ \"]" '{print $7,$8}' | awk -F"['?']" '{a[$1]++}END{for (i in a) print a[i],i}' | sort -nr > ${five_txt}
#cat ${LOG_FILE} | grep "${C_DATE}" | awk -F'\"' '$10>10' | awk -F"[ \"]" '{print $7,$8}' | awk -F"['?']" '{a[$1]++}END{for (i in a) print a[i],i}'| sort -nr  > ${ten_txt}

main() {
  if [[ $(cat ${five_txt} | wc -l) -ge 1 ]]; then
    echo "{" >${TMPFILE}
    echo "  \"msgtype\": \"markdown\"," >>${TMPFILE}
    echo "  \"markdown\": {" >>${TMPFILE}
    echo "    \"content\": \"<font color=\\\"warning\\\">**${DOMAIN}-001** 慢速接口统计，检查是否与新上线功能有关。-- ${C_DATE}</font>\n" >>${TMPFILE}
    echo "    > 响应时间**大于5s**的接口如下：\n" >>${TMPFILE}
    while read line
    do
      echo "   <font color=\\\"comment\\\">$line</font>\n" >>${TMPFILE}
    done < ${five_txt}
    if [[ $(cat ${ten_txt} | wc -l) -ge 1 ]]; then
      echo "    > 响应时间**大于10s**的接口如下：\n" >>${TMPFILE}
      while read line
      do
        echo "   <font color=\\\"comment\\\">$line</font>\n" >>${TMPFILE}
      done < ${ten_txt}
    fi
    printf "\"" >>${TMPFILE}
    echo "  }" >>${TMPFILE}
    echo "}" >>${TMPFILE}

    curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx' -H 'Content-Type: application/json' -d @${TMPFILE}
  fi
}

main