#!/bin/sh
#Created by AukeyIT
set -eu

DATE=`date +%Y%m%d`
dbpath=/data/dbbackup

#: mysql user
user='root'

#: mysql password
passwd = ''

dbname=`mysql -u$user -p$passwd -e "show databases;" |egrep -v "Database|mysql|performance_schema|information_schema|test|zabbix|logs|sys" > $dbpath/dblist.txt`

#: remote host info
remoteuser='root'
remotehost=''

#: remote backup path
currnet_ip=`ifconfig eth0 |grep "inet addr"|sed -n '/inet addr/s/^[^:]*:\([0-9.]\{7,15\}\) .*/\1/p'`
remotepath=/data/remote_mysql_bak/$currnet_ip
remotepasswd=''

######backup
db_bak() {
cd $dbpath
mkdir $DATE
cd $DATE
for db in `cat $dbpath/dblist.txt`
do
mysqldump -u"$user" -p"$passwd" -R --opt "$db" > "$dbpath"/"$DATE"/"$db"_"$DATE".sql
tar czf "$db"_"$DATE".tar.gz "$db"_"$DATE".sql
rm -f "$db"_"$DATE".sql
sleep 1
expect_remote
sleep 2
done
}
########
expect_remote(){
/usr/bin/expect -c"
set timeout 100;
spawn /usr/bin/scp -r "$dbpath"/"$DATE"/"$db"_"$DATE".tar.gz "$remoteuser"@"$remotehost":"$remotepath"/"$DATE"
expect {
\"*yes/no*\" {send \"yes\r\"; exp_continue}
\"*password*\" {send "\"'123456'"\r\";}
}
expect eof;"
}
########
expect_mkdir(){
/usr/bin/expect <<-EOF
set time 30
spawn ssh $remoteuser@${remotehost}
expect {
"*yes/no" { send "yes\r"; exp_continue }
"*password:" { send "$remotepasswd\r" }
}
expect "*#"
send "cd /data/remote_mysql_bak/$currnet_ip\r"
expect "*#"
send "mkdir $DATE\r"
expect "*#"
send "exit\r"
interact
expect eof
EOF
}
#######
expect_mkdir
db_bak
#######del old db backup
find /data/dbbackup -mtime +7 |grep .tar.gz |xargs rm -f
