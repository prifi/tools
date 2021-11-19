#!/usr/bin/env bash
set -uo pipefail
# Describe: Auto Block Spider IP For Nginx. --20211117
flag=0

trap 'rm -f "$TMPFILE"' EXIT
TMPFILE=$(mktemp) || exit 1

# base info
NGX_HOME="/data/service/nginx"
DOMAIN=$(hostname | sed -r 's/(.*)-(.*)-(.*)/\2/')
LOG_FILE="${NGX_HOME}/logs/${DOMAIN}.com_443_access.log"

# block nginx file
C_DATE=$(date +%Y%m%d)
O_DATE=$(date -d '-15 days' +%Y%m%d)  # unblock for 15 days ago.
BLOCK_DIR="${NGX_HOME}/conf/auto_block_ip_map"
[ -d "${BLOCK_DIR}" ] || mkdir -p "${BLOCK_DIR}"

BLOCK_FILE="${BLOCK_DIR}/${C_DATE}.conf"
BLOCK_OLD_FILE="${BLOCK_DIR}/${O_DATE}.conf"

file_txt="${C_DATE}.txt"

# alert values
max_load=25
max_ng_conn=1500
max_ng_perip_requets=1000

# current values
curr_ng_conn=$(netstat -an |grep ':443\b' |grep 'ESTABLISHED'| wc -l)
curr_load=$(uptime |awk -F'[: ,]+' '{printf "%.0f",$14}')

# filter time range
sec=$(date +%s)
c_time=$(date -d @"${sec}" +'%d/%b/%Y:%H:%M:%S')
e_time=$(date -d @"$((sec-300))" +'%d/%b/%Y:%H:%M:%S')

# test values
#curr_ng_conn=4000
#curr_load=50
#e_time="16/Nov/2021:15:50:00"
#c_time="16/Nov/2021:15:55:00"

block_action() {
  if [[ $curr_ng_conn -ge $max_ng_conn || $curr_load -ge $max_load ]]; then
    if [[ ! -f "${file_txt}" ]]; then
      cat "${LOG_FILE}" | awk -F"[ '[']*" '$4 >= "'$e_time'" && $4 <= "'$c_time'" {print $NF}' | cut -d"." -f1-3 | cut -d":" -f1-3 | \
        awk '{a[$1]++} END {for(i in a) print a[i], "\t", i}' | grep -Ev "127.0.0" | awk '$1>='$max_ng_perip_requets' {print $2}' | while read line
      do
        if [[ -n $line ]]; then
          echo $line > ${file_txt}
        fi
      done

      if [[ -f "${file_txt}" ]]; then
        let flag+=1
      fi
    else
      c_count=$(cat ${file_txt} | wc -l)

      cat "${LOG_FILE}" | awk -F"[ '[']*" '$4 >= "'$e_time'" && $4 <= "'$c_time'" {print $NF}' | cut -d"." -f1-3 | cut -d":" -f1-3 | \
        awk '{a[$1]++} END {for(i in a) print a[i], "\t", i}' | grep -Ev "127.0.0" | awk '$1>='$max_ng_perip_requets' {print $2}' | while read line
      do
        if [[ $(grep -c "$line" "${file_txt}") -eq '0' ]]; then
          echo $line >> ${file_txt}
        fi
      done

      e_count=$(cat ${file_txt} | wc -l)

      if [[ $e_count -gt $c_count ]]; then
        let flag+=1
      fi
    fi
  fi
}

unblock_action() {
  if [ -f "${BLOCK_OLD_FILE}" ]; then
    rm -f "${BLOCK_OLD_FILE}" && "${NGX_HOME}"/sbin/nginx -t
    [ $? -eq 0 ] && systemctl reload nginx || exit 1;
  fi
}

main() {
  if [[ $flag -ne 0 ]]; then
    cat ${file_txt} | awk 'BEGIN {printf "map $realip $black {\n    default \"\";\n"} {print "   ","~"$1,"1;"} END {print "}"}' > ${BLOCK_FILE}

    if [ -f "${BLOCK_FILE}" ]; then
      "${NGX_HOME}"/sbin/nginx -t
      [ $? -eq 0 ] && systemctl reload nginx || exit 1;

      echo "{" >${TMPFILE}
      echo "  \"msgtype\": \"markdown\"," >>${TMPFILE}
      echo "  \"markdown\": {" >>${TMPFILE}
      echo "    \"content\": \"<font color=\\\"warning\\\">**${DOMAIN}** 站点最近5分站爬虫请求大于${max_ng_perip_requets}，已自动添加屏蔽。</font>\n" >>${TMPFILE}
      echo "    ><font color=\\\"comment\\\"> ${BLOCK_FILE}</font>\n" >>${TMPFILE}
      while read line
      do
        echo "   <font color=\\\"comment\\\">$line</font>\n" >>${TMPFILE}
      done < ${file_txt}
      printf "\"" >>${TMPFILE}
      echo "  }" >>${TMPFILE}
      echo "}" >>${TMPFILE}

      curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/xxx' -H 'Content-Type: application/json' -d @${TMPFILE}
    fi
  fi
}

block_action
unblock_action
main