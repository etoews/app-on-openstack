#!/usr/bin/env bash

apt-get -y -qqq update; apt-get -y -qqq upgrade
apt-get -y -qqq install git python-pip

echo "source /root/api_env.rc" >> /root/.profile
echo "source /root/db_env.rc" >> /root/.profile
source /root/.profile

git clone https://github.com/$GITHUB_USERNAME/app-on-openstack.git /root/app-on-openstack
pip install virtualenv
virtualenv api-venv
source api-venv/bin/activate
pip install -r /root/app-on-openstack/code/api/requirements.txt
python /root/app-on-openstack/code/api/manage.py runserver --host 0.0.0.0 &
