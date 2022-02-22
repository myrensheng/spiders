import time
import requests

# 财联社滚动文章的数据接口
base_url = "https://www.cls.cn/nodeapi/updateTelegraphList"
# 获取前 10 分钟内刷新的消息
last_time = int(time.time() - 60 * 10)
# 构造请求参数
params = {
    "app": "CailianpressWeb",
    "category": "",
    "hasFirstVipArticle": 1,
    "lastTime": str(last_time),
    "os": "web",
    "rn": "20",
    "subscribedColumnIds": "",
    "sv": "7.5.5",
    "sign": "9fa0d3f7fcb3d39a4ca734c543f99d03",
}
# 构造请求头
header = {
    "Host": "www.cls.cn",
    "Connection": "keep-alive",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    "Accept": 'application/json, text/plain, */*',
    "sec-ch-ua-mobile": '?0',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Content-Type": "application/json;charset=utf-8",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.cls.cn/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "HWWAFSESID=2d39e9747745a7ca5e; HWWAFSESTIME=1620959717642; hasTelegraphRemind=on; hasTelegraphSound=on; vipNotificationState=on; Hm_lvt_fa5455bb5e9f0f260c32a1d45603ba3e=1620959719; hasTelegraphNotification=off; Hm_lpvt_fa5455bb5e9f0f260c32a1d45603ba3e=1620961307",
    "If-None-Match": 'W/"3f-WG/1HjmC3FTHAG8QCCJGb5w1iSY"',
}


def main():
    """
    获取数据的主函数
    :return: 获取的数据列表
    """
    # 请求 url，得到返回的数据
    res = requests.get(url=base_url, params=params, headers=header)
    # 如果返回状态码是 304 表示没有更新数据
    if res.status_code == 304:
        return "304 无数据更新"
    elif res.status_code == 200:
        # 返回状态码是 200 表示请求成功
        news_list = []
        # 将返回的 json 数据转为 dict 类型
        dict_res = dict(res.json())
        # 数据保存在 data-roll_data 中
        roll_data_list = dict_res["data"]["roll_data"]
        for roll_data in roll_data_list:
            # 保存需要的数据，文章时间，文章内容，文章简介
            dict_ = {
                "ctime": roll_data["ctime"],
                "content": roll_data["content"],
                "share_url": roll_data["shareurl"],
                "brief": roll_data.get("brief", "财联社"),
            }
            news_list.append(dict_)
        return news_list


if __name__ == '__main__':
    result = main()
    print(result)
