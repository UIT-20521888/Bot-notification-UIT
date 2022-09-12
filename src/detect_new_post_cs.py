from asyncore import read
from bs4 import BeautifulSoup as bs
import requests
import json
from datetime import datetime
from send_messebger import send_message
import asyncio
from detect_new_pots_ctsv import read_json,save_file,check
url='http://cs.uit.edu.vn'
def get_sourse(url):
    page=requests.get(url,verify=False)
    page_source=bs(page.content,'html.parser')
    return page_source
def filter_data(page_source):
    data=page_source.find(id='torch_home_blog-3')
    data=data.find_all(href=True)
    result=[]
    for i in data:
        if len(i['href'].split('/'))>7 and "Read More>>" not in i.text and i.text!='':
            save={'title':i.text,'link':i['href'][:-1]}
            result.append(save)
    return result
def detect_new_post(post_old,post_new):
    result = []
    for i in post_new:
        if check(i,post_old):
            result.append(i)
    if len(result)!=0:
        asyncio.run(send_message("Khoa Khoa Học Máy Tính có thông báo mới. Mời xem!!!"))
    for i in result:
        print(i['link'])
        asyncio.run(send_message(i['link']))
def run_cs(url,path_save):
    page_source=get_sourse(url)
    post_new=filter_data(page_source)
    post_old=read_json(path_save)
    detect_new_post(post_old,post_new)
    save_file(path_save,post_new)
run_cs(url,'./data/cs.json')

