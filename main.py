import requests
import shutil
import os
import zipfile
import subprocess


def check_and_get_data():
    url = f'https://api.github.com/repos/SagerNet/sing-box/releases'
    # subprocess.run(["winsw", "restart", "D:/Programs/winsw/singbox.xml"])
    # 发起 GET 请求获取仓库的所有 release
    response = requests.get(url, headers={'Accept': 'application/vnd.github.v3'})
    if response.status_code == 200:
        releases = response.json()

        # 遍历所有 release
        for release in releases:
            if release.get('prerelease'):
                assets = release.get('assets', [])

                # 提取每个 pre-release 的文件下载链接
                for asset in assets:
                    download_url = asset.get('browser_download_url')
                    if download_url and "windows-amd64v3" in download_url:
                        # 获取本地版本
                        url = 'http://127.0.0.1:9090/version'
                        response = requests.get(url)
                        local_version = response.json().get('version')
                        local_version = local_version.replace(' ', '-')
                        # 使用正则表达式匹配提取
                        if local_version not in download_url:
                            return download_url
                        else:
                            print("当前已是最新版本！")
                            return None
    print(response.json())
    return None


def down_extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows10; U; Windows NT 5.1; zh-CN) AppleWebKit./55.0.15 (KHTML, like) Chrome/91.0.4472'}
    sb_folder = "D:/Programs/singbox"
    # 下载压缩包
    response = requests.get(url)
    with open("singbox.zip", "wb") as f:
        f.write(response.content)
    print("最新内核文件下载成功，开始替换内核...")
    subprocess.run(["winsw", "stop", "D:/Programs/winsw/singbox.xml"])
    # 指定解压文件
    full_name = os.path.basename(url)
    split_name = os.path.splitext(full_name)[0]
    # 解压压缩包
    with zipfile.ZipFile("singbox.zip", "r") as z:
        target_assert = f"{split_name}/sing-box.exe"
        z.extract(target_assert, sb_folder)
        os.remove(f"{sb_folder}/sing-box.exe")
        shutil.move(f"{sb_folder}/{target_assert}", sb_folder)
        shutil.rmtree(f"{sb_folder}/{split_name}")

    subprocess.run(["winsw", "start", "D:/Programs/winsw/singbox.xml"])
    os.remove("singbox.zip")
    print("内核更新成功")


if __name__ == '__main__':
    down_url = check_and_get_data()
    print(down_url)
    if down_url:
        print("获取最新版本下载链接成功！开始下载内核...")
        down_extract(down_url)