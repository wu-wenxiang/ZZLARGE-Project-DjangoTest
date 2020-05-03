# https://github.com/wu-wenxiang/Doc-Common/blob/master/config-docker/Dockerfile

# Build folder
# FROM maodouzi/django:1.11.29
FROM registry.cn-shanghai.aliyuncs.com/99cloud-sh/django:1.11.29
RUN mkdir -p /home/www/mysite/logs \
    && mkdir -p /home/www/mysite/tool \
    && mkdir -p /home/www/mysite/src
WORKDIR /home/www/mysite
COPY mysite /home/www/mysite/src/mysite
COPY requirements.txt /home/www/mysite/src/mysite/requirements.txt
RUN rm -rf /home/www/mysite/src/mysite/initdb.py \
    && rm -rf /home/www/mysite/src/mysite/syncdb.py \
    && rm -rf /home/www/mysite/src/mysite/static \
    && rm -rf /home/www/mysite/src/mysite/data \
    && pip install -r /home/www/mysite/src/mysite/requirements.txt \
    && cd /home/www/mysite/src/mysite && python manage.py collectstatic

# Setup nginx
RUN rm -f /etc/nginx/sites-enabled/default
ADD docker-config/nginx.conf /etc/nginx/sites-available/mysite.conf
RUN ln -s /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/mysite.conf
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# # Setup supervisord
# RUN mkdir -p /var/log/supervisor
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# run sh. Start processes in docker-compose.yml
#CMD ["/usr/bin/supervisord"]
ADD docker-config/supervisord.conf /etc/supervisor/supervisord.conf
ADD docker-config/supervisor.conf /etc/supervisor/conf.d/mysite.conf
ADD docker-config/start.sh /tmp/start.sh
EXPOSE 80
CMD [ "sh", "/tmp/start.sh" ]
