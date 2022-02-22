import requests

url = "https://www.amazon.cn/dp/B09KRFM975/ref=pd_rhf_ee_s_pd_crbs_1/460-1666951-0551250?pd_rd_w=0vock&pf_rd_p=21aec615-5d56-438a-bf01-e07025538514&pf_rd_r=8AGC5Q4V09FAGWBHJTDH&pd_rd_r=85a265b4-5f2b-4618-9c7b-75c6a8eb3ba6&pd_rd_wg=pCjJJ&pd_rd_i=B09KRFM975&psc=1"

res = requests.get(url)
print(res.text)