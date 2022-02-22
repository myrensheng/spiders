import os
import string
import requests

# 百度图片搜索地址
url = "https://image.baidu.com/search/acjson"
# 构造请求头数据
header = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'image.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
# 构造请求参数
param = {
    'tn': 'resultjson_com',
    'ipn': 'rj',
    'ct': '201326592',
    'fp': 'result',
    'queryWord': '',
    'cl': '2',
    'lm': '-1',
    'ie': 'utf-8',
    'oe': 'utf-8',
    'st': '-1',
    'ic': '0',
    'word': '',
    'face': '0',
    'istype': '2',
    'nc': '1',
    'pn': '60',
    'rn': '30',
    'gsm': '1e',
}


def get_json(query_word=None, page_num=None):
    """
    根据查询的关键词及查询的页面返回 json 数据
    :param query_word: 输入的关键词
    :param page_num: 查询的页面数
    :return: 对应的 json 数据
    """
    # 参数列表中添加 queryWord 关键词
    param["queryWord"] = query_word
    param["word"] = query_word
    # 参数列表中添加 pn 关键词
    param["pn"] = f'{30 * page_num}'
    # 请求百度图片网站，将返回的 json 数据转换为 dict 数据
    res = requests.get(url=url, headers=header, params=param)
    res_dict = dict(res.json())
    return res_dict


def save_picture(query_word=None, pic_name=None, pic_url=None):
    """
    将图片保存在以 query_word 为名创建新的文件夹
    :param query_word:输入的关键词
    :param pic_name: json 中解析出来的图片名称
    :param pic_url: json 中解析出来的图片地址
    :return: None
    """
    # 获取当前 py 文件所在的绝对地址
    cwd = os.getcwd()
    # 拼接 images 文件夹地址
    images_path = os.path.join(cwd, "images")
    query_word_path = os.path.join(images_path, query_word)
    # 如果没有 images 文件夹，就新建一个
    if "images" not in os.listdir(cwd):
        os.mkdir(images_path)
    # 在 images 文件夹下，新建以 query_word 为名的文件夹
    if query_word not in os.listdir(images_path):
        os.mkdir(query_word_path)
    # 根据 pic_url 读取图片
    pic = requests.get(pic_url, stream=True)
    # 构造图片地址
    pic_path = os.path.join(query_word_path, pic_name)
    # 保存图片
    with open(pic_path, "wb") as f:
        for c in pic.iter_content(chunk_size=10240):
            f.write(c)


def get_pic_info(res=None):
    """
    解析 get_json 函数返回的 json 数据
    :param res: get_json 函数返回的 json 数据
    :return: 重新构造的图片数据，包含图片名称，图片地址
    """
    # 多张图片的信息列表
    pic_info = []
    # 图片数据存放在 data 中
    for data in res["data"]:
        # 获取图片名称
        pic_name = data.get("fromPageTitleEnc", None)
        # 获取图片地址
        pic_url = data.get("hoverURL", None)
        # 判断图片名称和图片地址是否存在
        if pic_name and pic_url:
            # 替换图片名称中的特殊字符
            pic_name = pic_name.replace(" ", '')
            for p in string.punctuation:
                pic_name = pic_name.replace(p, '')
            # 用图片名称命名图片
            if "png" in pic_url:
                pic_name += ".png"
            if "jpg" in pic_url:
                pic_name += ".jpg"
            if "gif" in pic_url:
                pic_name += ".gif"
            if "jpeg" in pic_url:
                pic_name += ".jpeg"
            if "bmp" in pic_url:
                pic_name += ".bmp"
            else:
                pic_name += ".jpg"
            pic_info.append({"pic_name": pic_name, "pic_url": pic_url})
    return pic_info


def main():
    # 程序运行的主函数
    while True:
        # 多次下载，直到输入 q 退出
        query_word = str(input("输入要下载的图片名（q退出）："))
        if query_word == "q":
            break
        while True:
            # 当输入的数量不为整数，循环输入
            pic_num = input("输入需要下载的页数（q退出）：")
            if pic_num == "q":
                break
            try:
                pic_num = int(pic_num)
            except:
                continue
            # 下载量不超过 30 就下载第一页图片
            page_num = 1 if int(pic_num / 30) == 0 else int(pic_num / 30)
            for i in range(1, page_num + 1):
                # 获取 json 数据
                res = get_json(query_word=query_word, page_num=i)
                # 获取图片名和图片地址
                pic_info = get_pic_info(res=res)
                # 保存图片
                for pic in pic_info:
                    print(pic["pic_name"], "下载完成")
                    save_picture(query_word=query_word, pic_name=pic["pic_name"], pic_url=pic["pic_url"])
            break


if __name__ == '__main__':
    main()
