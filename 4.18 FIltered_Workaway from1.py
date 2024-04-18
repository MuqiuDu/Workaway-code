import requests
import time
from parsel import Selector
import re
import os
import json
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from langdetect import detect

def check_is_english(text):
    try:
        lang = detect(text)
        if lang == 'en':
            return text
        else:
            return ''
    except:
        pass
    return text

W_Review_P_List = []

def append_to_json(filename, item):
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = []
        
    h_urls = []
    for _ in json_data:
        h_urls.append(_.get('H_url'))
    if item['H_chargers_fee'] == '' and  item['feedback_data'] != [] and item['feedback_data'] != [[]] :
        del item['H_chargers_fee']
        if item['H_url'] not in h_urls:
            json_data.append(item)
        else:
            return
    else:
        return

    with open(filename, 'w', encoding='utf-8-sig') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

def read_file(filename):
    with open(filename, 'r',encoding='utf-8-sig') as file:
        data = json.load(file)
    item_urls = []
    for d_item in data:
        item_urls.append(d_item['H_url'])
    return data,item_urls

def get_host_data(s1_x,url):
    try:
        H_Nation_new = s1_x('//li[@title="Country"]/div[@class="profile-title-list-text"]//text()').get().strip()
    except:
        H_Nation_new =''
    try:
        H_WorkHours_new = s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Hours expected"]/../../../p/text()').get()
    except:
        H_WorkHours_new =''
    try:
        H_No_helperAccommodate_new = s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="How many Workawayers can stay?"]/../../../p/text()').get()
    except:
        H_No_helperAccommodate_new =''
    try:
        H_MoreInformation_new = ', '.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="A little more information"]/../../../ul/li[not(@style)]//text()').getall())
    except:
        H_MoreInformation_new =''
    try:
        H_chargers_fee_new = s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="This host charges a fee"]/..//div[@class="alert alert-warning"]/text()').get()
        if H_chargers_fee_new == None:
            H_chargers_fee_new = ''
    except:
        H_chargers_fee_new =''
    return H_Nation_new,H_WorkHours_new,H_No_helperAccommodate_new,H_MoreInformation_new,H_chargers_fee_new

def get_user_data(user_url):
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive','DNT': '1',
        'Pragma': 'no-cache',
        'Referer': 'https://www.workaway.info/en/host/895776687753',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
  
    response3 = requests.get(user_url,headers=headers,)
    time.sleep(1)
    select3 = Selector(response3.text)
    s3_x = select3.xpath
    try:
        W_Nation = s3_x('//ul[@class="profile-title-list"]/li[1]/div[@class="profile-title-list-text"]/text()').get().strip()
    except:
        W_Nation = ''
    try:
        W_Age = s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="Age"]/../p//text()').get().strip()
    except:
        W_Age =''
    W_Age = W_Age.replace('\n','').replace(' ','')
    try:
        W_ReviewScore = len(s3_x('//div[@class="profile-section-title"]/div[@class="row gutter-6"]/div[@class="col-xs-5"]//a/i[@class="fa fa-star yellow-text"]'))
    except:
        W_ReviewScore = '0'
    
    return W_Nation,W_Age,W_ReviewScore

def get_feedback_data(s1_x):
    global W_Review_P_List

    feedback_data2 = []
    workawayer_Review = []
    host_Review = []
    for ww in s1_x('//div[@id="section-profile-feedback"]/div[@class="profile-content-box"]//div[@class="feedback_content feedback_content_ww"]'):
        W_Review = len(ww.xpath('./../../div[@class="feedback-thumb-wrapper"]//i[@class="fa fa-star yellow-text"]').getall())
        if W_Review >5:W_Review = 5
        W_Review_P = ''
        for _ in ww.xpath('./div[@class="feedback_msg_ww"]//text()').getall():
            W_Review_P += _.strip()
            W_Review_P = check_is_english(W_Review_P)
        if W_Review_P != '':
            if W_Review_P not in W_Review_P_List:
                result = re.findall(r'[A-Za-z\s]+', W_Review_P)
                if result:
                    user_name = ww.xpath('.//div[@class="row text-muted"]//div[@class="col-sm-8 col-sm-pull-4"]/small/a/text()').get()
                    user_url = ww.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-8 col-sm-pull-4"]//a/@href').get()
                    DateReview = ww.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-4 col-sm-push-8"]//text()').get().strip()
               
                    if user_url != None:
                        user_url = 'https://www.workaway.info' + user_url
                        W_Nation,W_Age,W_ReviewScore = get_user_data(user_url)
                    else:
                        W_Nation,W_Age,W_ReviewScore = '','',''
                        user_url = ''
                    workawayer_Review.append({
                        'W_Review':W_Review,
                        'W_Review_P':W_Review_P,
                        'DateReview':DateReview,
                        'W_Nation':W_Nation,
                        'W_Age':W_Age,
                        'W_ReviewScore':W_ReviewScore,
                        'user_name':user_name,
                        'user_url':user_url,
                    })
                    W_Review_P_List.append(W_Review_P)

    feedback_data2.append(workawayer_Review)
    return feedback_data2
    
def get_one_data(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive','DNT': '1',
        'Pragma': 'no-cache',
        'Referer': 'https://www.workaway.info/en/host/981375591437/feedback',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    response1 = requests.get(url,  headers=headers,)
    time.sleep(0.1)
    select1 = Selector(response1.text)
    s1_x = select1.xpath
    
    H_Nation,H_WorkHours,H_No_helperAccommodate,H_MoreInformation,H_chargers_fee = get_host_data(s1_x,url)
    feedback_data =  get_feedback_data(s1_x)

    item = {
        'H_Nation':H_Nation,
        'H_WorkHours':H_WorkHours,
        'H_No_helperAccommodate':H_No_helperAccommodate,
        'H_MoreInformation':H_MoreInformation,
        'H_chargers_fee':H_chargers_fee,
        'H_url':url,
        'feedback_data':feedback_data,
        
    }
    return item

def first_get(start_category='40'):
    c_list = ['36','38','37','31','18','40','1','14','34','29','17','28','33','35','19','39']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive','DNT': '1',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    start = False
    for c in c_list:
        if c == start_category:
            start = True
        if not start:
            continue
        print(f'正在爬取第{c}类')
        for page in range(1,501):
            
            params = {
                'hidden': '',
                'showMoreOptions': '0',
                'search': '',
                'lang': 'en',
                'workawayer_capacity': '0',
                'languages': '',
                'date_start': '',
                'date_end': '',
                'min_stay': '',
                'c[]': c,
                'host_rating': '0',
                'country': '',
                'region': '',
                'gnid': '',
                'lat': '0',
                'lon': '0',
                'ct': '',
                'distance': '',
                'all': '1',
                'Page': str(page),
            }
            
            response = requests.get('https://www.workaway.info/en/hostlist', params=params, headers=headers,)
            time.sleep(1)
            select = Selector(response.text)
            
            urls = [ 'https://www.workaway.info' + _ for _ in select.xpath('//a[@class="listentry-title"]/@href').getall()]
            for url in urls:
                print(f'正在爬取第{c}类，第{page}页。{url}')
                time.sleep(0.1)
                item = get_one_data(url)
                append_to_json(filename, item)

# 保存文件名  
filename = '4.18Filtered_workaway.json'        
first_get(start_category='40')
