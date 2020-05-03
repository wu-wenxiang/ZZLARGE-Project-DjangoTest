#!/bin/bash

[ -f /home/www/mysite/src/mysite/data/init.sh ] && sh /home/www/mysite/src/mysite/data/init.sh

cron
nginx
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
