#!/usr/bin/env bash

rm -rf /tmp/v2ray_v3.tar.gz
tar zcf /tmp/v2ray_v3.tar.gz ./v2ray_v3
scp /tmp/v2ray_v3.tar.gz us4:/tmp/

if [ $? -ne 0 ]; then
    echo "scp fail"
    exit -1
fi
ssh us4 "pkill v2ray;rm -rf /root/v2ray_v3/;tar zxf /tmp/v2ray_v3.tar.gz -C /root/;nohup /root/v2ray_v3/v2ray >/dev/null 2>&1 &"
if [ $? -ne 0 ]; then
    echo "ssh fail"
    exit -1
fi

pkill v2ray
nohup ./v2ray_v2/v2ray >/dev/null 2>&1 &
nohup ./v2ray_v1/v2ray >/dev/null 2>&1 &
