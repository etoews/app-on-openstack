#!/usr/bin/env bash

apt-get -y -qq update; apt-get -y -qq upgrade
apt-get -y -qq install haproxy

IFS=$'\n\t'
source /root/api_ips.rc

for IP in ${WM_API_IPS[@]}; do
  echo "        server app $IP" >> /root/lb.haproxy
done

cp /root/lb.haproxy /etc/haproxy/haproxy.cfg
service haproxy restart


git clone https://github.com/$GITHUB_USERNAME/app-on-openstack.git /root/app-on-openstack
pip install virtualenv
virtualenv /root/app-venv
source /root/app-venv/bin/activate
pip install -r /root/app-on-openstack/code/app/requirements.txt
cd /root/app-on-openstack/code/app; gunicorn manage:app -b localhost:8000 &

/etc/init.d/nginx start
rm /etc/nginx/sites-enabled/default
cp /root/app-on-openstack/code/app/app.nginx /etc/nginx/sites-available/app
ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app
/etc/init.d/nginx restart
