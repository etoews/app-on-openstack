#!/usr/bin/env bash

apt-get -y -qq update; apt-get -y -qq upgrade
apt-get -y -qq install git python-pip

echo "source /root/api_env.rc" >> /root/.profile
echo "source /root/db_env.rc" >> /root/.profile
source /root/.profile

git clone https://github.com/$GITHUB_USERNAME/app-on-openstack.git /root/app-on-openstack
pip install virtualenv
virtualenv /root/api-venv
source /root/api-venv/bin/activate
pip install -r /root/app-on-openstack/code/api/requirements.txt
python /root/app-on-openstack/code/api/manage.py runserver --host 0.0.0.0 &
