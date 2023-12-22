import base64
import json
import os
import shutil
import time
import logging
from datetime import datetime

import requests
from bypy import ByPy


# 设置日志
logging.basicConfig(filename='backup_by_BaiDuYun.log', level=logging.INFO)


def backup_blog(prefix, port, user, password, backup_path):
    # 网站地址
    website = f"http://localhost:{port}"
    # halo2备份文件夹路径
    backup_halo_path = f"/data/blog/{prefix}/backups"

    backup_api = website + f"/apis/migration.halo.run/v1alpha1/backups"
    check_api = website + f"/apis/migration.halo.run/v1alpha1/backups?sort=metadata.creationTimestamp%2Cdesc"

    # 获取现在的时间 2023-09-24T13:14:18.650Z
    now_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    logging.info(now_time)
    # 构建认证头部
    auth_header = "Basic " + base64.b64encode((user + ":" + password).encode()).decode()
    payload = json.dumps({
        "apiVersion": "migration.halo.run/v1alpha1",
        "kind": "Backup",
        "metadata": {
            "generateName": "backup-",
            "name": ""
        },
        "spec": {
            "expiresAt": now_time,
        }
    })
    headers = {
        'User-Agent': '',
        'Content-Type': 'application/json',
        'Authorization': "Basic " + base64.b64encode((user + ":" + password).encode()).decode(),
    }
    response = requests.request("POST", backup_api, headers=headers, data=payload)
    logging.info(response.text)
    if response.status_code == 201:
        logging.info(f"{prefix}备份请求成功！")
        while True:
            check_response = requests.request("GET", check_api, headers=headers)
            if check_response.status_code == 200:
                backup_data = json.loads(check_response.text)
                items = backup_data.get("items", [])
                if items[0]["status"]["phase"] == "SUCCEEDED":
                    logging.info(f"{prefix}备份完成！")
                    new_backup_name = items[0]["status"]["filename"]
                    break
                if items[0]["status"]["phase"] == "RUNNING":
                    logging.info(f"{prefix}正在备份！")
                    time.sleep(10)

            else:
                logging.error(f"{prefix}查询备份请求失败！错误代码：{check_response.status_code}")
        shutil.copy(backup_halo_path + "/" + new_backup_name, backup_path + "/" + new_backup_name)
        logging.info(f"{prefix}备份文件复制完成！")

    else:
        logging.error(f"{prefix}备份请求失败！错误代码：{response.status_code}")


def ignore_sock_files(dirname, filenames):
    return [name for name in filenames if name.endswith('.sock')]


def backup_mysql(backup_path):
    # 复制MySQL数据
    dst_path = backup_path + "/mysql"
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    shutil.copytree("/data/mysql", dst_path, ignore=ignore_sock_files)


def backup_redis(backup_path):
    # 复制Redis数据
    dst_path = backup_path + "/redis"
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    shutil.copytree("/data/redis", dst_path, ignore=ignore_sock_files)


def zip_and_upload(directory):
    # 打包并上传到百度云
    shutil.make_archive(directory, 'zip', directory)
    bp = ByPy()
    bp.upload(localpath=directory + ".zip", remotepath="/backup/" + directory + ".zip", ondup='overwrite')
    # 删除原始文件夹
    shutil.rmtree(directory)
    logging.info(f"{directory} has been deleted after zipping and uploading.")


if __name__ == '__main__':
    # 创建日期文件夹
    date_folder = "/backup/" + datetime.now().strftime('%Y-%m-%d')
    os.makedirs(date_folder, exist_ok=True)

    # 调用函数进行备份
    blogs = [('博客', '端口号', '管理员用户名', '管理员密码'), ('博客', '端口号', '管理员用户名', '管理员密码'),
             ('博客', '端口号', '管理员用户名', '管理员密码'), ('博客', '端口号', '管理员用户名', '管理员密码')]
    for prefix, port, user, password in blogs:
        os.makedirs(f"{date_folder}/halo/{prefix}", exist_ok=True)
        backup_blog(prefix, port, user, password, f"{date_folder}/halo/{prefix}")

    # 备份MySQL和Redis
    backup_mysql(date_folder)
    backup_redis(date_folder)

    # 打包并上传所有备份
    zip_and_upload(date_folder)