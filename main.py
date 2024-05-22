import re

import requests
import os
import zipfile
import subprocess


def check_and_get_data():
    url = f'https://api.github.com/repos/MetaCubeX/mihomo/releases/tags/Prerelease-Alpha'
    # subprocess.run(["winsw", "restart", "D:/Programs/winsw/singbox.xml"])
    # 发起 GET 请求获取仓库的所有 release
    response = requests.get(url, headers={'Accept': 'application/vnd.github.v3'})
    if response.status_code == 200:
        releases = response.json()
        assets = releases['assets']
        for asset in assets:
            download_url = asset.get('browser_download_url')
            if download_url and "windows-amd64-alpha" in download_url:
                # 获取远程版本
                asset_name = asset.get('name')
                version_pattern = r"alpha-[0-9a-zA-Z]+"
                version_match = re.search(version_pattern, asset_name)
                remote_version = ""
                if version_match:
                    remote_version = version_match.group()
                    print(f"远程核心版本: {remote_version}")
                else:
                    print("远程核心版本未找到")
                # 获取本地版本
                url = 'http://127.0.0.1:9090/version'
                response = requests.get(url)
                local_version = response.json().get('version')
                local_version = local_version.replace(' ', '-')
                print(f"本地核心版本: {local_version}")
                if local_version != remote_version:
                    return download_url
                else:
                    print("当前核心已是最新！")
                    return None


def down_extract(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows10; U; Windows NT 5.1; zh-CN)'
                      ' AppleWebKit./55.0.15 (KHTML, like) Chrome/91.0.4472'}
    sb_folder = "D:/Programs/mihomo"
    # 下载压缩包
    response = requests.get(url, headers=headers)
    with open("mihomo.zip", "wb") as f:
        f.write(response.content)
    print("最新内核文件下载成功，开始替换内核...")
    subprocess.run(["winsw", "stop", "D:/Programs/winsw/mihomo.xml"])
    # 解压压缩包
    with zipfile.ZipFile("mihomo.zip", "r") as z:
        target_assert = f"mihomo-windows-amd64.exe"
        z.extract(target_assert, sb_folder)

    subprocess.run(["winsw", "start", "D:/Programs/winsw/mihomo.xml"])
    os.remove("mihomo.zip")
    print("内核更新成功")


if __name__ == '__main__':
    down_url = check_and_get_data()
    if down_url:
        print(f"获取最新版本下载链接成功！开始下载内核...\n{down_url}")
        down_extract(down_url)
    input("任意键退出...")