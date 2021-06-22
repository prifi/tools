!/bin/bash
#
DATE=$(date +%Y-%m-%d%H%M%S)
OLDDATE=$(date +%Y-%m-%d%H%M%S --date="-20 days")

MYSQL="/data/service/mysql/bin/mysql -uroot -p -h127.0.0.1"
[ -d /data/backup/db/$DATE ] || mkdir -p /data/backup/db/$DATE
cd /data/backup/db/$DATE

for table in `$MYSQL aecmp-web -e "show tables"|sed '1d'`
do
    /data/service/mysql/bin/mysqldump -uroot -p'' -h127.0.0.1 --opt aecmp-web $table |gzip >$table.sql.gz
done
