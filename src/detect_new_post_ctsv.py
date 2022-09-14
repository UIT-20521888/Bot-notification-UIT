from asyncore import read
from bs4 import BeautifulSoup as bs
import requests
import json
from datetime import datetime
from send_messebger import send_message
import asyncio
url='https://ctsv.uit.edu.vn'
def filter_link(page_source):
    all_link=page_source.find(id='main-content')
    all_link=all_link.find_all("tr")
    # print(len(all_link))
    # for link in all_link:
    #     print(link)
    #     print(".................................\n")
    return all_link
class post_uit:
    def __init__(self,link,title,date):
        self.link=link
        self.title=title
        self.date=date

def get_all_post(all_post):
    # print(all_post)
    result_proc_text=[]
    for post in all_post:
        proc_post=[text for text in post.text.split('\n') if text!=""]
        # print(proc_post)
        result_text=[]
        for text in proc_post:
            proc_text=""
            for i in text.split(' '):
                if i=="" or i=="-":
                    continue
                proc_text=proc_text+i+" "
            result_text.append(proc_text[:-1])
        link=url+post.find(href=True)["href"]
        result_text_js={"title":result_text[0], "link":link,"date":result_text[1]}
        result_proc_text.append(result_text_js)
    return result_proc_text
        #     result_proc_text.append(proc_text)
    # print(result_proc_text)
    # print("................................................\n")
# def save_file(list_result):
def read_json(path):
    with open(path,'r', encoding='utf-8') as f:
        data=json.load(f)
    return data['data']
def save_file(path_file,data):
    data_save={"data":data}
    with open(path_file, 'w',encoding='utf-8') as f:
        json.dump(data_save, f,ensure_ascii=False,indent=4)
def check(i, data):
    if i in data:
        return False
    else:
        return True

def detect_new_post(path_file,all_post_new):
    data_read=read_json(path_file)
    result=[]
    for i in all_post_new:
        if check(i,data_read):
            result.append(i)
    # print(result)
    if len(result)!=0:
        asyncio.run(send_message("Phòng CTSV có thông báo mới. Mời xem!!!"))
    for i in result:
         asyncio.run(send_message(i['link']))
    sorted_list = sorted(all_post_new, key=lambda t: datetime.strptime(t["date"], '%d/%m/%Y'))
    save_file(path_file,sorted_list)
def run_ctsv(url,path_file):
    page=requests.get(url,verify=False)
    page_source=bs(page.content,'html.parser')
    detect_new_post(path_file,get_all_post(filter_link(page_source)))
run_ctsv(url,"./data/ctsv.json")
