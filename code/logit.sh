#!/usr/bin/env bash

# Print all logs to console
# Run this script from <my-username>-deploy-server

IFS=$'\n\t'

source /root/app_ips.rc

for IP in ${WM_IPS[@]}; do
  echo "*** App $IP ***"
  ssh -i ~/.ssh/id_rsa.qcon_deploy root@$IP cat app-on-openstack/code/app/wm_app.log
done

source /root/api_ips.rc

for IP in ${WM_IPS[@]}; do
  echo "*** API $IP ***"
  ssh -i ~/.ssh/id_rsa.qcon_deploy root@$IP cat app-on-openstack/code/api/wm_api.log
done

source /root/worker_ips.rc

for IP in ${WM_IPS[@]}; do
  echo "*** Worker $IP ***"
  ssh -i ~/.ssh/id_rsa.qcon_deploy root@$IP cat app-on-openstack/code/worker/wm_worker.log
done
