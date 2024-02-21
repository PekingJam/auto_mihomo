import requests
import re
import os
import zipfile
import subprocess
import time


def check_and_get_data():
    url = f'https://api.github.com/repos/MetaCubeX/mihomo/releases'
    subprocess.run(["winsw", "restart", "D:/Programs/winsw/mihomo.xml"])
    # 发起 GET 请求获取仓库的所有 release
    response = requests.get(url)
    if response.status_code == 200:
        releases = response.json()

        # 遍历所有 release
        for release in releases:
            if release.get('prerelease'):
                assets = release.get('assets', [])

                # 提取每个 pre-release 的文件下载链接
                for asset in assets:
                    download_url = asset.get('browser_download_url')
                    if download_url and "windows-amd64-alpha" in download_url:
                        # 获取本地版本
                        url = 'http://127.0.0.1:9090/version'
                        response = requests.get(url)
                        local_version = response.json().get('version')
                        # 使用正则表达式匹配提取
                        match = re.search(r'(clash|alpha)-(.*?)\.zip', download_url)
                        remote_version = f"{match.group(1)}-{match.group(2)}"
                        print(f"本地版本{local_version},最新版本{remote_version}")
                        if local_version != remote_version:
                            return download_url
                        else:
                            print("当前已是最新版本！")
    return None


def down_extract(url):
    # 下载压缩包
    response = requests.get(url)
    with open("mihomo.zip", "wb") as f:
        f.write(response.content)
    print("最新内核文件下载成功，开始替换内核...")
    subprocess.run(["winsw", "stop", "D:/Programs/winsw/mihomo.xml"])
    # 解压压缩包
    with zipfile.ZipFile("mihomo.zip", "r") as z:
        z.extractall("D:/Programs/mihomo")
    subprocess.run(["winsw", "start", "D:/Programs/winsw/mihomo.xml"])
    os.remove("mihomo.zip")
    print("内核更新成功")


if __name__ == '__main__':
    down_url = check_and_get_data()
    if down_url:
        print("获取最新版本下载链接成功！开始下载内核...")
        down_extract(down_url)