import os
import time
import requests
from bs4 import BeautifulSoup

# 2010统计年鉴导航栏页面
html_url = "http://www.stats.gov.cn/tjsj/pcsj/rkpc/6rp/lefte.htm"
# 下载 excel 的基础地址
base_url = "http://www.stats.gov.cn/tjsj/pcsj/rkpc/6rp/"


def spider():
    # 获取页面源码
    html = requests.get(html_url)
    # 更改页面编码为 gb2312
    html.encoding = "gb2312"
    # 使用 bs4 解析页面
    soup = BeautifulSoup(html.text, 'lxml')
    # 获取页面中所有的 a 标签，返回列表数据
    a_soup = soup.find_all("a")
    for a in a_soup:
        # 获取 a 标签中的 href 属性值
        href = a.get("href")
        # href 中包含 excel 字样的为正确的文件地址
        if "excel" in href:
            # 拼接 url 地址，获取 excel 文件
            result = requests.get(base_url + href)
            # 使用 a 标签的 text 属性命名 excel 文件
            excel_name = os.path.join(os.getcwd(), "excels", a.text + ".xlsx")
            # 将 excel 文件写入同级目录下的 excels 文件夹
            with open(excel_name, "wb") as f:
                f.write(result.content)
            print(a.text, "完成")
            time.sleep(2)
            break


if __name__ == '__main__':
    # 如果统计目录下没有 excels 文件夹，就创建一个
    if "excels" not in os.listdir():
        os.mkdir(os.path.join(os.getcwd(),"excels"))
    # 开始下载
    spider()
