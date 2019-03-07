#!/usr/bin/env python

import json
import os
import sys
import uuid
import pathlib
import string
import random

ss_password = ''.join(random.sample(string.printable*32, 32))
id = str(uuid.uuid4())

v_1_config = {
  "inbounds": [
    {
      "port": 1080, # 监听端口
      "listen": "127.0.0.1", 
      "protocol": "socks", # 入口协议为 SOCKS 5
      "settings": {
        "auth": "noauth"  # 不认证
      },
      "sniffing": {
        "enabled": False,
        "destOverride": ["http", "tls"]
      },
    }
  ],

  "outbounds": [
    {
      "protocol": "shadowsocks",
      "settings": {
        "servers": [
          {
            "address": "127.0.0.1", # Shadowsocks 的服务器地址
            "method":"aes-256-cfb", # Shadowsocks 的加密方式
            "ota": True, # 是否开启 OTA，True 为开启
            "password": ss_password, # Shadowsocks 的密码
            "port": 1081
          }
        ]
      }
    }
  ]
}


v_2_config = {
  "inbounds": [
    {
      "port": 1081, # 监听端口
      "listen": "0.0.0.0",
      "protocol": "shadowsocks",

      "settings": {
        "method": "aes-256-cfb",
        "ota": True,
        "password": ss_password, 
      }
    }
  ],

    "outbounds": 
    [
        {
          "protocol": "vmess", # 出口协议
          "settings": {
          "vnext": [
          {
            "address": "67.230.177.19", # 服务器地址，请修改为你自己的服务器 IP 或域名
            "port": 21,  # 服务器端口
            "users": [
              {
                "id": id,  # 用户 ID，必须与服务器端配置相同
                "alterId": 64 # 此处的值也应当与服务器相同
              }
            ]
          }
        ]
          }
        }
    ]
}

v_3_config = {
  "inbounds":[
    { #主端口配置
      "port": 21,
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "id": id,
            "alterId": 64
          }
        ],
        "detour": { #绕行配置，即指示客户端使用 dynamicPort 的配置通信
          "to": "dynamicPort"   
        }
      }
    },
    {
      "protocol": "vmess",
      "port": "10000-60000", # 端口范围
      "tag": "dynamicPort",  # 与上面的 detour to 相同
      "settings": {
        "default": {
          "alterId": 64
        }
      },
      "allocate": {            # 分配模式
        "strategy": "random",  # 随机开启
        "concurrency": 23,      # 同时开放两个端口,这个值最大不能超过端口范围的 1/3
        "refresh": 3           # 每三分钟刷新一次
      }
    }
  ],

    "outbounds": [
	{
	  "protocol": "freedom",
	  "settings": {}
	}
      ]
}

for i in range(3):
    pathdir = pathlib.Path(f'v2ray_v{i}')    
    os.system(f'rm -rf {pathdir}')
    os.system(f'cp -r v2ray {pathdir}')
    config = f'v_{i}_config'
    config_output_path = pathdir / 'config.json'
    with open(config_output_path, 'w') as cf:
        json.dump(config, cf, indent=4)

os.system('cat tmp.json')
