crontab /home/www/mysite/src/mysite/data/crontab.txt

echo DB_GIT_URL=\"${DB_GIT_URL}\" > /root/env.sh
echo DB_SECRET=\"${DB_SECRET}\" >> /root/env.sh

git config --global user.email "wu-wenxiang@outlook.com"
git config --global user.name "Wenxiang Wu"
