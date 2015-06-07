#!/usr/bin/env bash

apt-get -y -qq update; apt-get -y -qq upgrade
apt-get -y -qq install python-pip git nginx

echo "source /root/api_env.rc" >> /root/.profile
echo "source /root/db_env.rc" >> /root/.profile
echo "source /root/os_env.rc" >> /root/.profile
source /root/.profile

git clone https://github.com/everett-toews/app-on-openstack.git /root/app-on-openstack
pip install virtualenv
virtualenv /root/api-venv
source /root/api-venv/bin/activate
pip install -r /root/app-on-openstack/code/api/requirements.txt
cd /root/app-on-openstack/code/api; gunicorn manage:app -b localhost:8000 &

/etc/init.d/nginx start
rm /etc/nginx/sites-enabled/default
cp /root/app-on-openstack/code/api/api.nginx /etc/nginx/sites-available/api
ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/api
/etc/init.d/nginx restart
