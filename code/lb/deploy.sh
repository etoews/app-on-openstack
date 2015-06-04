#!/usr/bin/env bash

apt-get -y -qq update; apt-get -y -qq upgrade
apt-get -y -qq install haproxy

IFS=$'\n\t'
source /root/ips.rc

for IP in ${WM_IPS[@]}; do
  echo "        server app $IP" >> /root/lb.haproxy
done

cp /root/lb.haproxy /etc/haproxy/haproxy.cfg
service haproxy restart
