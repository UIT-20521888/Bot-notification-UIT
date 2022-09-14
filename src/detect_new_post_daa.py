from asyncore import read
from bs4 import BeautifulSoup as bs
import requests
import json
from datetime import datetime
from send_messebger import send_message
import asyncio
from detect_new_post_ctsv import read_json,save_file,check
from detect_new_post_cs import get_sourse
url='https://student.uit.edu.vn'
def filter_data(page_sourse,url):
    data_chung=page_sourse.find(id='block-views-hien-thi-bai-viet-moi-block')
    data_noibat=page_sourse.find(id='block-views-tin-noi-bat-block')
    post_chung=data_chung.find_all(href=True)
    result=[]
    for item in post_chung[:-1]:
        link=url+item['href']
        post={'title':item.text,'link':link}
        if post not in result:
            result.append(post)
    post_noibat=data_noibat.find_all(href=True)
    for item in post_noibat[:-1]:
        link=url+item['href']
        post={'title':item.text,'link':link}
        if post not in result:
            result.append(post)
    # print(result)
    return result
def detect_new_post_daa(post_old,post_new):
    result = []
    for item in post_new:
        if check(item,post_old):
            result.append(item)
    if len(result)!=0:
        asyncio.run(send_message("Phòng đào tạo có thông báo mới. Mời xem!!!"))
    for i in result:
        print(i['link'])
        asyncio.run(send_message(i['link']))
def run_daa(url,path_file):
    page_source=get_sourse(url)
    post_new=filter_data(page_source,url)
    post_old=read_json(path_file)
    detect_new_post_daa(post_old,post_new)
    save_file(path_file,post_new)
run_daa(url,'./data/daa.json')

