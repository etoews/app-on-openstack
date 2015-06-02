#!/usr/bin/env bash

apt-get -y update; apt-get -y upgrade
apt-get -y install git python-pip

echo "source $HOME/api_env.rc" >> $HOME/.profile
echo "source $HOME/db_env.rc" >> $HOME/.profile
source $HOME/.profile

git checkout https://github.com/$GITHUB_USERNAME/app-on-openstack.git
pip install virtualenv
virtualenv api-venv
source api-venv/bin/activate
pip install -r $HOME/app-on-openstack/code/api/requirements.txt
python $HOME/app-on-openstack/code/api/watermark/api.py runserver