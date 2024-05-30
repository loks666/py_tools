import json

import requests

# 列表中的每一个域名执行一次请求
domains = [
    "superxiang.com",
    "img.superxiang.com",
    "blog.superxiang.com",
    "aiblog.superxiang.com",
    "ry.superxiang.com",
    "pay.superxiang.com",
    "one.superxiang.com",
    "fly.superxiang.com",
    "new.superxiang.com",
    "lobe.superxiang.com",
    "next.superxiang.com",
    "fastgpt.superxiang.com",
    "chatnio.superxiang.com",
    "coze.superxiang.com",
]

# 请求模板
request_template = {
    "type": "http",
    "name": "",
    "parent": 6,
    "url": "",
    "method": "GET",
    "interval": 60,
    "retryInterval": 60,
    "resendInterval": 0,
    "maxretries": 3,
    "timeout": 48,
    "notificationIDList": {"1": True},
    "ignoreTls": False,
    "upsideDown": False,
    "packetSize": 56,
    "expiryNotification": True,
    "maxredirects": 10,
    "accepted_statuscodes": ["200-299"],
    "dns_resolve_type": "A",
    "dns_resolve_server": "1.1.1.1",
    "docker_container": "",
    "docker_host": None,
    "proxyId": None,
    "mqttUsername": "",
    "mqttPassword": "",
    "mqttTopic": "",
    "mqttSuccessMessage": "",
    "authMethod": None,
    "oauth_auth_method": "client_secret_basic",
    "httpBodyEncoding": "json",
    "kafkaProducerBrokers": [],
    "kafkaProducerSaslOptions": {"mechanism": "None"},
    "kafkaProducerSsl": False,
    "kafkaProducerAllowAutoTopicCreation": False,
    "gamedigGivenPortOnly": True,
}

for domain in domains:
    # 复制请求模板并填充域名
    request_data = request_template.copy()
    request_data["name"] = domain
    request_data["url"] = f"https://{domain}"

    # 发送请求
    response = requests.post(
        "https://mon.superxiang.com/socket.io/?EIO=4&transport=polling&t=OreSrq0&sid=A_Vf_rB4OEjj5k6mAAAM",
        data=json.dumps([424, "add", request_data]), verify=False
    )

    # 检查响应
    if response.status_code == 200:
        print(f"Successfully created {domain}")
    else:
        print(f"Failed to create {domain}: {response.status_code}")
