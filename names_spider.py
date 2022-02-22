import time
import random
import requests
import sqlite3
from bs4 import BeautifulSoup


def get_name_link():
    # 解析百家姓列表，获取姓名对应的地址
    url = "http://www.resgain.net/xmdq.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    name_links = []
    for s in soup.find_all(attrs={'class': 'btn btn2'}):
        name_links.append("http:" + s.get('href'))
    return name_links


def get_data(url):
    # 连接数据库
    con = sqlite3.connect(r'tools_app.db')
    cursor = con.cursor()
    # 获取数据，并解析数据
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    if "boy" in url:
        sex_ = "男"
    else:
        sex_ = "女"
    for s in soup.find_all(attrs={'class': 'btn btn-default btn-lg namelist'}):
        name = s.find(attrs={'class': 'livemsg'}).get('data-name')
        sql = "insert into RANDOM_NAME (name,sex) values('{0}','{1}');".format(name, sex_)
        cursor.execute(sql)
        con.commit()
    print(url, "完成")
    con.close()


def create_db():
    # 创建 sqlite3 数据库
    conn = sqlite3.connect(r"tools_app.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE RANDOM_NAME
           (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
           NAME           TEXT    NOT NULL,
           SEX         TEXT    NOT NULL);''')
    print("RANDOM_NAME database created successfully")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # 创建数据库和RANDOM_NAME表
    create_db()
    # 获取百家姓连接地址
    name_link_list = get_name_link()
    for name_link in name_link_list:
        # 拼接男生和女生的地址
        url_boys = name_link.replace("/name_list.html", "/name/boys.html")
        url_girls = name_link.replace("/name_list.html", "/name/girls.html")
        # 获取数据，并保存到 tools_app.db 中
        get_data(url_boys)
        # 每次获取完成后，随机暂停几秒
        t = random.randint(1, 3)
        time.sleep(t)
        get_data(url_girls)
        t = random.randint(1, 3)
        time.sleep(t)
        # break
