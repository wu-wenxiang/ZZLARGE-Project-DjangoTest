#!/usr/bin/env bash

. /root/env.sh

cd /root && [ ! -d /root/backup ] && git clone ${DB_GIT_URL} backup

[ -d /root/backup ] && cd /root/backup && rm -rf db.sqlite3 \
&& dd if=db.txt | openssl des3 -d -k "${DB_SECRET}"|tar zxf - \
&& [ "x$(diff db.sqlite3 /home/www/mysite/src/mysite/data/db.sqlite3)" != "x" ] \
&& rm -rf db.sqlite3 db.txt \
&& cp /home/www/mysite/src/mysite/data/db.sqlite3 db.sqlite3 \
&& tar -zcvf - db.sqlite3|openssl des3 -salt -k "${DB_SECRET}" | dd of=db.txt \
&& git commit -a -m "routinely update" \
&& git push
