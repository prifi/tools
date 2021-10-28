#!/bin/bash
#
set -eo pipefail

siteName=$1
siteIp=$2

renew_num=15
waring_num=10

archive_dir="/etc/letsencrypt/archive/"
live_dir="/etc/letsencrypt/live/"

script_dir=$(cd "$(dirname "$0")" && pwd)

sendFile="${script_dir}/set_bot_message"
botMessage="<font color=\\\"warning\\\">[ ${siteName} ] SSL自动续约失败，需手动处理！</font>\n"

[ -z $2 ] && (
    echo "Please input a arg(eg:$(basename $0) feelily-test.ivlii.com 10.1.1.71)"
    exit 1
)

[ -e ${archive_dir} -o -e ${live_dir} ] || (
    echo "--- No [ $1 ] Dir!!! ---"
    exit 1
)

rsync_ssl() {
    /bin/certbot renew --quiet

    ssh ${siteIp} "mkdir /etc/letsencrypt/{archive,live} -p"

    rsync -avzP "${archive_dir}/${siteName}" "${siteIp}:${archive_dir}"
    rsync -avzP "${live_dir}/${siteName}" "${siteIp}:${live_dir}"
    [ $? -eq 0 ] || (
        echo "--- Rsync error ---"
        exit 1
    )
    sleep 1
    ssh $siteIp "systemctl reload nginx"
}

query_end() {
    END_TIME=$(openssl s_client -servername ${siteName} -connect ${siteName}:443 -showcerts </dev/null 2>&1 | openssl x509 -noout -dates | grep 'After' | awk -F'=' '{print $2}' | awk '{print $1,$2,$4}')
    END_TIME1=$(date +%s -d "$END_TIME")

    NOW_TIME=$(date +%s -d "$(date "+%Y-%m-%d")")
    RST=$(((END_TIME1 - NOW_TIME) / (60 * 60 * 24)))
}

query_end
#RST=14
if [[ ${RST} -le ${renew_num} ]]; then
    rsync_ssl
fi

query_end
#RST=9
if [[ ${RST} -le ${waring_num} ]]; then
    echo "{" >${sendFile}
    echo "  \"msgtype\": \"markdown\"," >>${sendFile}
    echo "  \"markdown\": {" >>${sendFile}
    echo "    \"content\": \"${botMessage}\"" >>${sendFile}
    echo "  }" >>${sendFile}
    echo "}" >>${sendFile}
    curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/xxxx' -H 'Content-Type: application/json' -d @${sendFile}
fi
