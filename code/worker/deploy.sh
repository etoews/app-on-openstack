#!/usr/bin/env bash

apt-get -y -qq update; apt-get -y -qq upgrade
apt-get -y -qq install python3-dev python-pip git

echo "source /root/os_env.rc" >> /root/.profile
source /root/.profile

git clone https://github.com/$GITHUB_USERNAME/app-on-openstack.git /root/app-on-openstack
pip install virtualenv
virtualenv -p python3 /root/worker-venv
source /root/worker-venv/bin/activate
pip install -r /root/app-on-openstack/code/worker/requirements.txt
cd /root/app-on-openstack/code/worker; python watermark/worker.py &
