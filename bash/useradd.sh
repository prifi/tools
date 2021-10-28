#!/bin/bash
set -eo pipefail

usage() {
  printf "\n"
  printf "Usage: sh %s GROUP USER" "$0"
  printf "\n GROUP \t 用户组：xxx|xxx "
  printf "\n USER \t 用户名：zhangs"
  printf "\n\n"
}

GROUP="$1"
USER="$2"
PASS=$(head /dev/urandom | cksum | md5sum | cut -c 1-8)
USER_DIR="$(pwd)/users"

[ -d "${USER_DIR}" ] || mkdir "$USER_DIR"

[ ! -n "${USER}" ] && (
  usage
  exit 1
)

test_user_group() {
  if [[ $(grep -w "${GROUP}" /etc/group | wc -l) -ne 1 ]] || [[ $(grep -w "${USER}" /etc/passwd | wc -l) -ne 0 ]]; then
    echo "Group or User input error!!"
    exit 1
  fi
}

test_samba_user() {
  pdbedit -L | grep -w "$USER"
  [ $? -eq 0 ] && (
    echo "Samba user [ $USER ] already exists!!"
    [ -f "${USER_DIR}/${USER}.txt" ] && cat ${USER_DIR}/${USER}.txt
    exit 1
  )
}

add_system_user() {
  test_user_group
  useradd -M -d /data/share -s /sbin/nologin -g "${GROUP}" -G bestwo "${USER}" >/dev/null 2>&1
  [ $? -eq 0 ] || (
    echo "Create system user error!!"
    exit 1
  )
  echo
}

add_samba_user() {
  #  test_samba_user
  echo -e "${PASS}\n${PASS}" | smbpasswd -a -s "${USER}"
  [ $? -eq 0 ] || (
    echo "Create samba user error!!"
    exit 1
  )
}

add_system_user
add_samba_user

cat <<EOF | tee ${USER_DIR}/${USER}.txt
xx开通信息

地址：\\\\xxx
用户：${USER}
密码：${PASS}
教程：xxx
EOF

mail -s "xx开通信息" "${USER}@xxx.com" <${USER_DIR}/${USER}.txt
[ $? -eq 0 ] || "Send Mail fail!!"
