#!/usr/bin/env bash

apt-get -y -qq update; apt-get -y -qq upgrade
apt-get -y -qq install haproxy

IFS=$'\n\t'
source /root/ips.rc

cat <<EOF >> /etc/haproxy/haproxy.cfg

listen  web-proxy 0.0.0.0:80
        mode http
        balance roundrobin
EOF

for IP in ${WM_IPS[@]}; do
  echo "        server app $IP" >> /etc/haproxy/haproxy.cfg
done

service haproxy restart
