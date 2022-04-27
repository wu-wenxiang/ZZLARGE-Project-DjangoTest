crontab /home/www/mysite/src/mysite/data/crontab.txt

echo DB_GIT_URL=\"${DB_GIT_URL}\" > /root/env.sh
echo DB_SECRET=\"${DB_SECRET}\" >> /root/env.sh

mkdir /root/.ssh
cp /home/www/mysite/src/mysite/data/id_rsa /root/.ssh/
chmod 0600 /root/.ssh/id_rsa

echo '
Host *
StrictHostKeyChecking no
UserKnownHostsFile=/dev/null' > /root/.ssh/config

git config --global user.email "wu-wenxiang@outlook.com"
git config --global user.name "Wenxiang Wu"
