from asyncore import read
from bs4 import BeautifulSoup as bs
import requests
import json
from datetime import datetime
from send_messenger import send_message
from detect_new_post_cs import get_sourse
import asyncio
from detect_new_post_ctsv import read_json,save_file,check
url="https://forum.uit.edu.vn/node/30"
def filter_link(page_source):
    data=page_source.find(id='topic-tab')
    data=data.find("table")
    data=data.find_all('tbody')
    data_post=data[1].find_all('tr')
    all_post=[]
    for post in data_post:
        post=post.find_all('td')[1]
        post=post.find_all('div')[0]
        post=post.find_all('a')[0]
        link=post['href']
        title=post.text
        new_post={'title':title,'link':link}
        all_post.append(new_post)
    # print(all_post)
    return all_post
def detect_new_post_forum(post_new,post_old):
    result=[]
    for i in post_new:
        if check(i,post_old):
            result.append(i)
    if len(result)!=0:
        asyncio.run(send_message("Forum có học bổng mới. Mời xem!!!"))
        print(result)
    for i in result:
        # print(i['link'])
        asyncio.run(send_message(i['link']))
def run_forum(url,path_save):
    page_source=get_sourse(url)
    post_new=filter_link(page_source)
    post_old=read_json(path_save)
    detect_new_post_forum(post_new,post_old)
    save_file(path_save,post_new)
run_forum(url,'./data/forum.json')