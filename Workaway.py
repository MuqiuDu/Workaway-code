import requests
import time
from parsel import Selector
import re
import os
import json
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

H_Review_P_List = []
def append_to_json(filename, item):
    
    # 读取JSON文件追加内容
    try:
        with open(filename, 'r',encoding='utf-8-sig') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = []
        
    h_urls = []
    for _ in json_data:
        h_urls.append(_.get('H_url'))
    if item['H_chargers_fee'] == '' and item['feedback_data'] != []:
        if item['H_url'] not in h_urls:
            json_data.append(item)
        else:
            return
    else:
        return
    # 将更新后的内容写入JSON文件
    with open(filename, 'w',encoding='utf-8-sig') as file:
        json.dump(json_data, file, indent=4,ensure_ascii=False)

def read_file(filename1,filename2):
    # 读取JSON文件
    with open(filename1, 'r',encoding='utf-8-sig') as file:
        data1 = json.load(file)
    with open(filename2, 'r',encoding='utf-8-sig') as file:
        data2 = json.load(file)
    item_urls = []
    for d_item in data1:
        item_urls.append(d_item['H_url'])
    return data1,data2,item_urls


def get_availability(id):
    # 获取host信息H_Availabilitya
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
    
    params = {
        'call': 'getHostCalendar',
        'y': '2024',
        'id': id,
    }
    time.sleep(1)
    response2 = requests.get('https://www.workaway.info/report_request.php', params=params,headers=headers,)
    select2 = Selector(response2.text)
    availability = ','.join([ _.replace('hostcalmonthinner dt2024','') for _ in select2.xpath('//div[@class="row"]//div[@class="calendar_green"]/../@class').getall()])
    return availability


def get_host_data(s1_x,url):
    # 爬取host主页信息
    H_ReviewScore_new = len(s1_x('//div[@class="col-xs-5"]//a/i[@class="fa fa-star yellow-text"]'))
    if H_ReviewScore_new  >5:H_ReviewScore_new  = 5
    try:
        H_No_Review_new = re.findall('(\d+)',s1_x('//div[@class="col-xs-5"]//a//text()').get())[0]
    except:
        H_No_Review_new=''
    try:
        H_Title_new = s1_x('//div[@class="profile-section-title"]/h1/text()').get().strip()
    except:
        H_Title_new = ''
    try:
        H_Nation_new = s1_x('//li[@title="Country"]/div[@class="profile-title-list-text"]//text()').get().strip()
    except:
        H_Nation_new =''
    try:
        H_Favoured_new = re.findall('\d+',s1_x('//ul[@class="profile-title-list"]/li[@title=""]//text()').get().strip())[0]
    except:
        H_Favoured_new = ''
    try:
        H_LastMinute_new = s1_x('//div[@class="row gutter-6"]/div[@class="col-xs-7 text-right"]/span[@class="badge bg-orange-light"]/text()').get()
    except:
        H_LastMinute_new = ''
    try:
        H_Photos_new = ','.join([_.replace('/thumb/','/xl/') for _ in s1_x('//div[@class="profile-header-masonry-wrapper"]//img/@src').getall()])
    except:
        H_Photos_new = ''
    try:
        H_MinumStay_new = ''.join(s1_x('//div[@id="hostcalendar"]/p[@class="text-muted"]/text()').getall()).replace('\xa0','')
    except:
        H_MinumStay_new = ''
    try:
        H_Availabilitya_new = get_availability(url.split('/')[-1])
        if H_Availabilitya_new == '':
            H_Availabilitya_new = get_availability(url.split('/')[-1])
    except:
        H_Availabilitya_new =''
    try:
        H_rate_new = s1_x('//h2[text()=" Host rating"]/../p/text()').get()
        if H_rate_new != None:
            H_rate_new = H_rate_new.replace('\n','').replace(' ','').strip()
    except:
        H_rate_new = ''
        
    try:
        H_ReplyRate_new = s1_x('//h2[text()="Reply rate"]/../p/text()').get()
        if H_ReplyRate_new != None:
            H_ReplyRate_new = H_ReplyRate_new.replace('\n','').replace(' ','').strip()
    except:
        H_ReplyRate_new = ''
        
    try:
        H_ReplyRate_p_new = s1_x('//h2[text()="Reply rate"]/../../../div[@class="profile-details-list-item-body"]/p/text()').get()
        if H_ReplyRate_p_new != None:
            H_ReplyRate_p_new = H_ReplyRate_p_new.replace('\n','').strip()
    except:
        H_ReplyRate_p_new = ''
    
    try:
        H_Feedback_new = s1_x('//h2[text()="Feedback"]/../p/text()').get()
        if H_Feedback_new != None:
            H_Feedback_new = H_Feedback_new.replace('\n','').replace(' ','').strip()
    except:
        H_Feedback_new = ''
    
    
    try:
        facebook_verified_new = s1_x('//h2[text()="Facebook verified"]').get()
        if facebook_verified_new == None:
            facebook_verified_new = ''
        else:
            facebook_verified_new = 'Yes'
    except:
        facebook_verified_new = ''
    
    
    try:
        email_verified_new = s1_x('//h2[text()="Email verified"]').get()
        if email_verified_new == None:
            email_verified_new = ''
        else:
            email_verified_new = 'Yes'
    except:
        email_verified_new = ''
    
    
    try:
        id_verified_new = s1_x('//h2[text()="ID verified"]').get()
        if id_verified_new == None:
            id_verified_new = ''
        else:
            id_verified_new = 'Yes'
    except:
        id_verified_new =''
    
    try:
        H_payment_new = s1_x('//h2[text()="Host offers payment"]').get()
        if H_payment_new == None:
            H_payment_new = ''
        else:
            H_payment_new = 'Yes'
    except:
        H_payment_new =''
    
    try:
        H_Badges_new = re.findall('(\d+)',s1_x('//div[@class="col-md-4 col-md-push-8"]//div[@class="profile-content-box"][2]//h2[@class="profile-content-box-title nomargin"]/text()').get())[0] + ' badges.(' +  ','.join(s1_x('//div[@class="col-md-4 col-md-push-8"]//div[@class="profile-content-box"][2]//div[@class="scroll-horizontal"]//div[@data-toggle="tooltip"]/@data-original-title').getall())+')'
    except:
        H_Badges_new = ''
    
    try:
        H_Description_new = ''.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Description"]/../../../p//text()').getall())
    except:
        H_Description_new = ''
    
    try:
        H_HelpTypes_new = ', '.join([_.strip() for _ in s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Types of help and learning opportunities"]/../../../div[@class="col-md-6 col-sm-6 typeofhelp_display_category"]//text()').getall()]).replace('/ ','/')
    except:
        H_HelpTypes_new = ''
    
    try:
        H_SDG_new = ', '.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="UN sustainability goals this host is trying to achieve"]/..//div[@class="un-goal un-goal-assigned"]/img/@alt').getall())
        if H_SDG_new == None:
            H_SDG_new = ''
    except:
        H_SDG_new = ''
    if H_SDG_new == '':
        H_SDG_new = ', '.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="UN sustainability goals this host is trying to achieve"]/../div//div[@class="goal"]/@data-name').getall())
        if H_SDG_new == None:
            H_SDG_new = ''
    try:
        H_Learning_new = ''.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Cultural exchange and learning opportunities"]/../../../p//text()').getall())
    except:
        H_Learning_new = ''
    try:
        H_ChildrenInvolve_new = ''.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Projects involving children"]/../../../p//text()').getall())
    except:
        H_ChildrenInvolve_new = ''
    try:
        H_Help_new = ''.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Help"]/../../../p//text()').getall())
    except:
        H_Help_new =''
    try:
        H_Language_new = ', '.join([ _.strip() for _ in s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Languages"]/../../../p[1]/text()').getall()])
    except:
        H_Language_new =''
    try:
        H_LanguageExchange_new = '\n'.join([ _.strip() for _ in s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Languages"]/../../../p[2]/text()').getall()])
    except:
        H_LanguageExchange_new =''
    try:
        H_Accommodation_new = ''.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Accommodation"]/../../../p/text()').getall())
    except:
        H_Accommodation_new =''
    try:
        H_WhatElse_new = ''.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="What else ..."]/../../../p/text()').getall())
    except:
        H_WhatElse_new =''
    try:
        H_MoreInformation_new = ', '.join(s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="A little more information"]/../../../ul/li[not(@style)]//text()').getall())
    except:
        H_MoreInformation_new =''
    try:
        H_No_helperAccommodate_new = s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="How many Workawayers can stay?"]/../../../p/text()').get()
    except:
        H_No_helperAccommodate_new =''
    try:
        H_WorkHours_new = s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Hours expected"]/../../../p/text()').get()
    except:
        H_WorkHours_new =''
    H_RateProfile_xpath = """//div[@class="col-sm-4"]/p[text()="
                            Accuracy of profile:
                            "]/text()"""
    try:
        H_RateProfile_new = re.findall('\(.*?\)',s1_x(H_RateProfile_xpath).getall()[-1])[0].replace('(','').replace(')','')
    except:
        H_RateProfile_new=''
    H_RateCulturalExchange_xpath = """//div[@class="col-sm-4"]/p[text()="
                            Cultural exchange:
                            "]/text()"""
    try:
        H_RateCulturalExchange_new = re.findall('\(.*?\)',s1_x(H_RateCulturalExchange_xpath).getall()[-1])[0].replace('(','').replace(')','')
    except:
        H_RateCulturalExchange_new=''
    H_RateCommunication_xpath = """//div[@class="col-sm-4"]/p[text()="
                            Communication:
                            "]/text()"""
    try:
        H_RateCommunication_new = re.findall('\(.*?\)',s1_x(H_RateCommunication_xpath).getall()[-1])[0].replace('(','').replace(')','')
    except:
        H_RateCommunication_new=''
    try:
        H_chargers_fee_new = s1_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="This host charges a fee"]/..//div[@class="alert alert-warning"]/text()').get()
        if H_chargers_fee_new == None:
            H_chargers_fee_new = ''
    except:
        H_chargers_fee_new =''
    return H_ReviewScore_new,H_No_Review_new,H_Title_new,H_Nation_new ,H_Favoured_new,H_LastMinute_new,H_Photos_new,H_MinumStay_new,H_Availabilitya_new,H_rate_new,H_ReplyRate_new,H_ReplyRate_p_new,H_Feedback_new,facebook_verified_new,email_verified_new,id_verified_new,H_payment_new,H_Badges_new,H_Description_new,H_HelpTypes_new,H_SDG_new,H_Learning_new,H_ChildrenInvolve_new,H_Help_new,H_Language_new,H_LanguageExchange_new,H_Accommodation_new,H_WhatElse_new,H_MoreInformation_new,H_No_helperAccommodate_new,H_WorkHours_new,H_RateProfile_new,H_RateCulturalExchange_new,H_RateCommunication_new,H_chargers_fee_new


def get_user_data(user_url):
    # 获取用户信息
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
        W_ReviewScore = len(s3_x('//div[@class="profile-section-title"]/div[@class="row gutter-6"]/div[@class="col-xs-5"]//a/i[@class="fa fa-star yellow-text"]'))
        W_No_Review = re.findall('(\d+)',s3_x('//div[@class="profile-section-title"]/div[@class="row gutter-6"]/div[@class="col-xs-5"]//a/span//text()').get())[0]
    except:
        W_ReviewScore,W_No_Review = '0','0'
    try:W_Badges = re.findall('(\d+)',s3_x('//div[@class="col-md-4 col-md-push-8"]//div[@class="profile-content-box"]//h2[@class="profile-content-box-title nomargin"]/text()').getall()[0].strip())[0] + ' badges.(' +  ','.join(s3_x('//div[@class="col-md-4 col-md-push-8"]//div[@class="profile-content-box"]//div[@class="scroll-horizontal"]//div[@data-toggle="tooltip"]/@data-original-title').getall())+')'
    except:W_Badges=''
    try:
        W_photos = s3_x('//div[@class="profilepic-w-wrapper"]/div[@class="profilepic-w-inner"]/a/@href').get().strip()
    except:
        W_photos = ''
    try:
        W_Description = ''.join(s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="Description"]/../p//text()').getall()).strip()
    except:
        W_Description = ''
    try:
        W_interests = ', '.join([_.strip() for _ in s3_x('''//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="
                        Interests "]/../div[@class="btn-interest"]/text()''').getall()]).strip()
    except:
        W_interests = ''
    if W_interests == '':
        try:
             W_interests = ', '.join([_.strip() for _ in s3_x('''//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="\n                    Interests "]/../div[@class="btn-interest"]/text()''').getall()]).strip()
        except:
            W_interests = ''
    try:
        W_language = ', '.join([_.strip() for _ in s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="Languages spoken"]/../p//text()').getall()]).strip()
    except:
        W_language=''
    if W_language == '':
        try:
            W_language = ', '.join([_.strip() for _ in s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]//strong[text()="Languages spoken"]/../text()').getall()]).strip()
        except:
            W_language=''
    try:
        W_LanguageExchange = '\n'.join([ _.strip() for _ in s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="col-xs-9"]/h2[text()="Languages"]/../../../p[2]/text()').getall()]).strip()
    except:
        W_LanguageExchange = ''
    # user_skills_knowledge = '\n'.join(_.replace('\xa0','').strip() for _ in s3_x('''//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="Skills and knowledge I'd like to share or learn"]/../div[@class="types-of-help-display-box"]//text()''').getall()).strip()
    try:
        W_Skills = ', '.join([_.strip() for _ in s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="More details about your skills"]/../p//text()').getall()]).strip()
    except:
        W_Skills = ''
    try:
        W_Age = s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="Age"]/../p//text()').get().strip()
    except:
        W_Age =''
    try:
        W_Knowledge = ', '.join([_.strip() for _ in s3_x('''//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="Skills and knowledge I'd like to share or learn"]/../div[@class="types-of-help-display-box"]//text()''').getall()]).strip()
    except:
        W_Knowledge =''
    try:
        W_someinformation = s3_x('//ul[@class="media-list media-list-profile"]/li//div[@class="media-body"]/h2[text()="Some more information"]/../ul/li[not(@style)]//text()').get().strip()
    except:
        W_someinformation = ''
    # user_feedback = '\n'.join([ _.strip() for _ in s3_x('//div[@class="feedback-wrapper"]//div[@class="feedback_msg_h"]//text()').getall()]).replace('… read more','').strip()
    Workawayer_home_feedbacks = []
    for _h in s3_x('//div[@id="section-profile-feedback"]/div[@class="profile-content-box"]//div[@class="feedback_content feedback_content_h"]'):
        WH_Review = len(_h.xpath('./../../div[@class="feedback-thumb-wrapper"]/i').getall())
        if WH_Review >5:WH_Review = 5
        Workawayer_home_feedbacks.append({
            'WH_Review':WH_Review,
            'WH_Review_P':'\n'.join([ _.strip() for _ in _h.xpath('.//div[@class="feedback_msg_h"]//text()').getall()]).replace('… read more','').strip(),
            'DateReview':_h.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-4 col-sm-push-8"]//text()').get().strip(),
            'By':'Host'
        })
    for _h in s3_x('//div[@id="section-profile-feedback"]/div[@class="profile-content-box"]//div[@class="feedback_content feedback_content_ww"]'):
        WW_Review = len(_h.xpath('./../../div[@class="feedback-thumb-wrapper"]/i').getall())
        if WW_Review >5:WW_Review = 5
        Workawayer_home_feedbacks.append({
            'WW_Review':WW_Review,
            'WW_Review_P':'\n'.join([ _.strip() for _ in _h.xpath('.//div[@class="feedback_msg_ww"]//text()').getall()]).replace('… read more','').strip(),
            'DateReview':_h.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-4 col-sm-push-8"]//text()').get().strip(),
            'By':'Workawayer'
        })

    # return W_Nation,W_ReviewScore,W_No_Review,W_Badges,W-photos,W_Description,W_interests,W_language,W_LanguageExchange,user_skills_knowledge,W_Skills,W-Age,W_Knowledge,W_someinformation,user_feedback
    return W_Nation,W_ReviewScore,W_No_Review,W_Badges,W_photos,W_Description,W_interests,W_language,W_LanguageExchange,W_Skills,W_Age,W_Knowledge,W_someinformation,Workawayer_home_feedbacks

def get_feedback_data(s1_x):
    # 获取评论
    feedback_data = []
    for ww in s1_x('//div[@id="section-profile-feedback"]/div[@class="profile-content-box"]//div[@class="feedback_content feedback_content_ww"]'):
        W_Review = len(ww.xpath('./../../div[@class="feedback-thumb-wrapper"]//i').getall())
        if W_Review >5:W_Review = 5
        W_Review_P = ''
        for _ in ww.xpath('./div[@class="feedback_msg_ww"]//text()').getall():
            W_Review_P += _.strip()
        result = re.findall(r'[A-Za-z\s]+', W_Review_P)
        if result:
            user_name = ww.xpath('.//div[@class="row text-muted"]//div[@class="col-sm-8 col-sm-pull-4"]/small/a/text()').get()
            user_url = ww.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-8 col-sm-pull-4"]//a/@href').get()
            DateReview = ww.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-4 col-sm-push-8"]//text()').get().strip()
            if int(DateReview.split()[-1]) >= 2010:

                # 检查是否提供了用户的主页，有则爬取用户主页信息
                if user_url != None:
                    user_url = 'https://www.workaway.info' + user_url

                    W_Nation,W_ReviewScore,W_No_Review,W_Badges,W_photos,W_Description,W_interests,W_language,W_LanguageExchange,W_Skills,W_Age,W_Knowledge,W_someinformation,Workawayer_home_feedbacks = get_user_data(user_url)
                else:
                    W_Nation,W_ReviewScore,W_No_Review,W_Badges,W_photos,W_Description,W_interests,W_language,W_LanguageExchange,W_Skills,W_Age,W_Knowledge,W_someinformation,Workawayer_home_feedbacks = '','','','','','','','','','','','','',''
                H_Review,H_Review_P = '',''
                feedback_data.append({
                    'W_Review':W_Review,
                    'W_Review_P':W_Review_P,
                    'H_Review':H_Review,
                    'H_Review_P':H_Review_P,
                    'DateReview':DateReview,
                    'W_Nation':W_Nation,
                    'W_ReviewScore':W_ReviewScore,
                    'W_No_Review':W_No_Review,
                    'W_Badges':W_Badges,
                    'W_photos':W_photos,
                    'W_Description':W_Description,
                    'W_interests':W_interests,
                    'W_language':W_language,
                    'W_LanguageExchange':W_LanguageExchange,
                    'W_Skills':W_Skills,
                    'W_Age':W_Age,
                    'W_Knowledge':W_Knowledge,
                    'W_someinformation':W_someinformation,
                    'Workawayer_home_feedbacks':Workawayer_home_feedbacks,
                    'user_name':user_name,
                    'user_url':user_url,
                })
            else:continue
    #用于配对信息
    global H_Review_P_List
    for hh in s1_x('//div[@id="section-profile-feedback"]/div[@class="profile-content-box"]//div[@class="feedback_msg_h"]'):
        H_Review = len(hh.xpath('./../../../div[@class="feedback-thumb-wrapper"]//i').getall())
        if H_Review >5:H_Review = 5
        H_Review_P = ''
        for _ in hh.xpath('..//div[@class="feedback_msg_h"]//text()').getall():
            H_Review_P += _.strip()
        result = re.findall(r'[A-Za-z\s]+', H_Review_P)
        if result:
            if 'More than three' not in H_Review_P:
                if H_Review_P not in H_Review_P_List:
                    user_name = hh.xpath('./..//div[@class="row text-muted"]//div[@class="col-sm-8 col-sm-pull-4"]/small/a/text()').get()
                    if user_name == None:
                        user_name = ''
                    feedback_data_new = []
                    for _ in feedback_data:
                        if user_name != '':
                            if _['user_name'] == user_name :
                                _['H_Review'] = H_Review
                                _['H_Review_P'] = H_Review_P
                        
                        feedback_data_new.append(_)

                    feedback_data = feedback_data_new
                    H_Review_P_List.append(H_Review_P)

    # 配对信息 feedback_data1
    feedback_data1 = []
    for _ in feedback_data:
        if _['H_Review_P'] !='' or _['H_Review'] !='':
            feedback_data1.append(_)
    
    
    
    # host profile
    feedback_data2 = []
    workawayer_Review = []
    host_Review = []
    for ww in s1_x('//div[@id="section-profile-feedback"]/div[@class="profile-content-box"]//div[@class="feedback_content feedback_content_ww"]'):
        W_Review = len(ww.xpath('./../../div[@class="feedback-thumb-wrapper"]//i').getall())
        if W_Review >5:W_Review = 5
        W_Review_P = ''
        for _ in ww.xpath('./div[@class="feedback_msg_ww"]//text()').getall():
            W_Review_P += _.strip()
        result = re.findall(r'[A-Za-z\s]+', W_Review_P)
        if result:
            user_name = ww.xpath('.//div[@class="row text-muted"]//div[@class="col-sm-8 col-sm-pull-4"]/small/a/text()').get()
            user_url = ww.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-8 col-sm-pull-4"]//a/@href').get()
            DateReview = ww.xpath('.//div[@class="row text-muted"]/div[@class="col-sm-4 col-sm-push-8"]//text()').get().strip()
            if int(DateReview.split()[-1]) >= 2010:
                # 检查是否提供了用户的主页，有则爬取用户主页信息
                if user_url != None:
                    user_url = 'https://www.workaway.info' + user_url
                    W_Nation,W_ReviewScore,W_No_Review,W_Badges,W_photos,W_Description,W_interests,W_language,W_LanguageExchange,W_Skills,W_Age,W_Knowledge,W_someinformation,Workawayer_home_feedbacks = get_user_data(user_url)
                else:
                    W_Nation,W_ReviewScore,W_No_Review,W_Badges,W_photos,W_Description,W_interests,W_language,W_LanguageExchange,W_Skills,W_Age,W_Knowledge,W_someinformation,Workawayer_home_feedbacks = '','','','','','','','','','','','','',''
                    
                workawayer_Review.append({
                    'W_Review':W_Review,
                    'W_Review_P':W_Review_P,
                    'DateReview':DateReview,
                    'W_Nation':W_Nation,
                    'W_ReviewScore':W_ReviewScore,
                    'W_No_Review':W_No_Review,
                    'W_Badges':W_Badges,
                    'W_photos':W_photos,
                    'W_Description':W_Description,
                    'W_interests':W_interests,
                    'W_language':W_language,
                    'W_LanguageExchange':W_LanguageExchange,
                    'W_Skills':W_Skills,
                    'W_Age':W_Age,
                    'W_Knowledge':W_Knowledge,
                    'W_someinformation':W_someinformation,
                    'Workawayer_home_feedbacks':Workawayer_home_feedbacks,
                    'user_name':user_name,
                    'user_url':user_url,
                })
            else:continue
    feedback_data2.append(workawayer_Review)
    
    for hh in s1_x('//div[@id="section-profile-feedback"]/div[@class="profile-content-box"]//div[@class="feedback_msg_h"]'):
        H_Review = len(hh.xpath('./../../../div[@class="feedback-thumb-wrapper"]//i').getall())
        if H_Review >5:H_Review = 5
        H_Review_P = ''
        for _ in hh.xpath('..//div[@class="feedback_msg_h"]//text()').getall():
            H_Review_P += _.strip()
        result = re.findall(r'[A-Za-z\s]+', H_Review_P)
        if result:
            if 'More than three' not in H_Review_P:
                DateReview = hh.xpath('./..//div[@class="row text-muted"]//div[@class="small text-right text-left-xs"]/text()').get().strip()
                if int(DateReview.split()[-1]) >= 2010:
                    if H_Review_P not in H_Review_P_List:
                        host_Review.append({
                            'H_Review':H_Review,
                            'H_Review_P':H_Review_P,
                            'DateReview':DateReview,
                        })
                        feedback_data2.append(host_Review)
                        H_Review_P_List.append(H_Review_P)
                else:continue
    return feedback_data1,feedback_data2

def get_one_data(url):
    # 根据链接读取host里面内容
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
    time.sleep(1)
    select1 = Selector(response1.text)
    s1_x = select1.xpath

    H_ReviewScore,H_No_Review,H_Title,H_Nation ,H_Favoured,H_LastMinute,H_Photos,H_MinumStay,H_Availabilitya,H_rate,H_ReplyRate,H_ReplyRate_p,H_Feedback,facebook_verified,email_verified,id_verified,H_payment,H_Badges,H_Description,H_HelpTypes,H_SDG,H_Learning,H_ChildrenInvolve,H_Help,H_Language,H_LanguageExchange,H_Accommodation,H_WhatElse,H_MoreInformation,H_No_helperAccommodate,H_WorkHours,H_RateProfile,H_RateCulturalExchange,H_RateCommunication,H_chargers_fee = get_host_data(s1_x,url)
    feedback_data1,feedback_data2 =  get_feedback_data(s1_x)

    item1 = {
        'H_ReviewScore':H_ReviewScore,
        'H_No_Review': H_No_Review,
        'H_Title':H_Title,
        'H_Nation':H_Nation,
        'H_Favoured':H_Favoured,
        'H_LastMinute':H_LastMinute,
        'H_Photos':H_Photos,
        'H_MinumStay':H_MinumStay,
        'H_Availabilitya':H_Availabilitya,
        'H_rate':H_rate,
        'H_ReplyRate':H_ReplyRate,
        'H_ReplyRate_p':H_ReplyRate_p,
        'H_Feedback':H_Feedback,
        'Facebook verified':facebook_verified,
        'Email verified':email_verified,
        'ID verified':id_verified,
        'H_payment':H_payment,
        'H_Badges':H_Badges,
        'H_Description':H_Description,
        'H_HelpTypes':H_HelpTypes,
        'H_SDG':H_SDG,
        'H_Learning':H_Learning,
        'H_ChildrenInvolve':H_ChildrenInvolve,
        'H_Help':H_Help,
        'H_Language':H_Language,
        'H_LanguageExchange':H_LanguageExchange,
        'H_Accommodation':H_Accommodation,
        'H_WhatElse':H_WhatElse,
        'H_MoreInformation':H_MoreInformation,
        'H_No_helperAccommodate':H_No_helperAccommodate,
        'H_WorkHours':H_WorkHours,
        'H_RateProfile':H_RateProfile,
        'H_RateCulturalExchange':H_RateCulturalExchange,
        'H_RateCommunication':H_RateCommunication,
        'H_chargers_fee':H_chargers_fee,
        'feedback_data':feedback_data1,
        'H_url':url,
    }
    item2 = {
        'H_ReviewScore':H_ReviewScore,
        'H_No_Review': H_No_Review,
        'H_Title':H_Title,
        'H_Nation':H_Nation,
        'H_Favoured':H_Favoured,
        'H_LastMinute':H_LastMinute,
        'H_Photos':H_Photos,
        'H_MinumStay':H_MinumStay,
        'H_Availabilitya':H_Availabilitya,
        'H_rate':H_rate,
        'H_ReplyRate':H_ReplyRate,
        'H_ReplyRate_p':H_ReplyRate_p,
        'H_Feedback':H_Feedback,
        'Facebook verified':facebook_verified,
        'Email verified':email_verified,
        'ID verified':id_verified,
        'H_payment':H_payment,
        'H_Badges':H_Badges,
        'H_Description':H_Description,
        'H_HelpTypes':H_HelpTypes,
        'H_SDG':H_SDG,
        'H_Learning':H_Learning,
        'H_ChildrenInvolve':H_ChildrenInvolve,
        'H_Help':H_Help,
        'H_Language':H_Language,
        'H_LanguageExchange':H_LanguageExchange,
        'H_Accommodation':H_Accommodation,
        'H_WhatElse':H_WhatElse,
        'H_MoreInformation':H_MoreInformation,
        'H_No_helperAccommodate':H_No_helperAccommodate,
        'H_WorkHours':H_WorkHours,
        'H_RateProfile':H_RateProfile,
        'H_RateCulturalExchange':H_RateCulturalExchange,
        'H_RateCommunication':H_RateCommunication,
        'H_chargers_fee':H_chargers_fee,
        'feedback_data':feedback_data2,
        'H_url':url,
    }
    return item1,item2

def first_get():
    # 第一次爬取数据，第二次及以上也可以用这个
    c_list = ['36','38','37','31','18','40','1','14','34','29','17','28','33','35','19','39',]
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
    for c in c_list:
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
                print(f'正在爬取第{page}页。{url}')
                time.sleep(1)
                item1,item2 = get_one_data(url)
                append_to_json(filename1, item1)
                append_to_json(filename2, item2)
def check_changes(url,d_item,data1,data2,item_new1,item_new2):
    #检查是否有变化
    flag = False
    try:
        flag = any(d_item[key] != item_new1[key] for key in d_item.keys() if key != 'H_url')
    except:
        flag = True
    if flag:
        # 遍历列表，找到需要替换的字典元素，并进行替换操作
        for index, d_item in enumerate(data1):
            if d_item["H_url"] == url:
                data1[index] = item_new1

        for index, d_item in enumerate(data2):
            if d_item["H_url"] == url:
                data2[index] = item_new2
                
                
        # 保存回JSON文件
        with open(filename1, 'w',encoding='utf-8-sig') as file:
            json.dump(data1, file, indent=4,ensure_ascii=False)
        with open(filename2, 'w',encoding='utf-8-sig') as file:
            json.dump(data2, file, indent=4,ensure_ascii=False)
    return data1,data2
def modify_one_data(url,data1,data2):
    # 用于更新文件
    for d_item in data1:
        if d_item['H_url'] == url:
            break

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
    time.sleep(1)
    select1 = Selector(response1.text)
    s1_x = select1.xpath
    
    H_ReviewScore_new,H_No_Review_new,H_Title_new,H_Nation_new ,H_Favoured_new,H_LastMinute_new,H_Photos_new,H_MinumStay_new,H_Availabilitya_new,H_rate_new,H_ReplyRate_new,H_ReplyRate_p_new,H_Feedback_new,facebook_verified_new,email_verified_new,id_verified_new,H_payment_new,H_Badges_new,H_Description_new,H_HelpTypes_new,H_SDG_new,H_Learning_new,H_ChildrenInvolve_new,H_Help_new,H_Language_new,H_LanguageExchange_new,H_Accommodation_new,H_WhatElse_new,H_MoreInformation_new,H_No_helperAccommodate_new,H_WorkHours_new,H_RateProfile_new,H_RateCulturalExchange_new,H_RateCommunication_new,H_chargers_fee_new = get_host_data(s1_x,url)
    feedback_data_new1,feedback_data_new2 =  get_feedback_data(s1_x)
    
    item_new1 = {
        'H_ReviewScore':H_ReviewScore_new,
        'H_No_Review': H_No_Review_new,
        'H_Title':H_Title_new,
        'H_Nation':H_Nation_new,
        'H_Favoured':H_Favoured_new,
        'H_LastMinute':H_LastMinute_new,
        'H_Photos':H_Photos_new,
        'H_MinumStay':H_MinumStay_new,
        'H_Availabilitya':H_Availabilitya_new,
        'H_rate':H_rate_new,
        'H_ReplyRate':H_ReplyRate_new,
        'H_ReplyRate_p_new':H_ReplyRate_p_new,
        'H_Feedback':H_Feedback_new,
        'Facebook verified':facebook_verified_new,
        'Email verified':email_verified_new,
        'ID verified':id_verified_new,
        'H_payment':H_payment_new,
        'H_Badges':H_Badges_new,
        'H_Description':H_Description_new,
        'H_HelpTypes':H_HelpTypes_new,
        'H_SDG':H_SDG_new,
        'H_Learning':H_Learning_new,
        'H_ChildrenInvolve':H_ChildrenInvolve_new,
        'H_Help':H_Help_new,
        'H_Language':H_Language_new,
        'H_LanguageExchange':H_LanguageExchange_new,
        'H_Accommodation':H_Accommodation_new,
        'H_WhatElse':H_WhatElse_new,
        'H_MoreInformation':H_MoreInformation_new,
        'H_No_helperAccommodate':H_No_helperAccommodate_new,
        'H_WorkHours':H_WorkHours_new,
        'H_RateProfile':H_RateProfile_new,
        'H_RateCulturalExchange':H_RateCulturalExchange_new,
        'H_RateCommunication':H_RateCommunication_new,
        'H_chargers_fee_new':H_chargers_fee_new,
        'feedback_data':feedback_data_new1,
        'H_url':url,
    }
    item_new2 = {
        'H_ReviewScore':H_ReviewScore_new,
        'H_No_Review': H_No_Review_new,
        'H_Title':H_Title_new,
        'H_Nation':H_Nation_new,
        'H_Favoured':H_Favoured_new,
        'H_LastMinute':H_LastMinute_new,
        'H_Photos':H_Photos_new,
        'H_MinumStay':H_MinumStay_new,
        'H_Availabilitya':H_Availabilitya_new,
        'H_rate':H_rate_new,
        'H_ReplyRate':H_ReplyRate_new,
        'H_ReplyRate_p_new':H_ReplyRate_p_new,
        'H_Feedback':H_Feedback_new,
        'Facebook verified':facebook_verified_new,
        'Email verified':email_verified_new,
        'ID verified':id_verified_new,
        'H_payment':H_payment_new,
        'H_Badges':H_Badges_new,
        'H_Description':H_Description_new,
        'H_HelpTypes':H_HelpTypes_new,
        'H_SDG':H_SDG_new,
        'H_Learning':H_Learning_new,
        'H_ChildrenInvolve':H_ChildrenInvolve_new,
        'H_Help':H_Help_new,
        'H_Language':H_Language_new,
        'H_LanguageExchange':H_LanguageExchange_new,
        'H_Accommodation':H_Accommodation_new,
        'H_WhatElse':H_WhatElse_new,
        'H_MoreInformation':H_MoreInformation_new,
        'H_No_helperAccommodate':H_No_helperAccommodate_new,
        'H_WorkHours':H_WorkHours_new,
        'H_RateProfile':H_RateProfile_new,
        'H_RateCulturalExchange':H_RateCulturalExchange_new,
        'H_RateCommunication':H_RateCommunication_new,
        'H_chargers_fee_new':H_chargers_fee_new,
        'feedback_data':feedback_data_new2,
        'H_url':url,
    }
    data1,data2 = check_changes(url,d_item,data1,data2,item_new1,item_new2)
    return data1,data2
    
def modify_file():
    # 第二次及以上爬取数据，从网站最近更新上爬取
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive','DNT': '1',
        'Pragma': 'no-cache',
        'Referer': 'https://www.workaway.info/en/hostlist?hidden=&showMoreOptions=0&search=&lang=en&workawayer_capacity=0&languages=&date_start=&date_end=&min_stay=&host_rating=0&is_updated=1&country=&region=&gnid=&lat=0&lon=0&ct=&distance=&all=1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',   
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    for page in range(1,201):
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
            'host_rating': '0',
            'is_updated': '1',
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
        
        response = requests.get('https://www.workaway.info/en/hostlist', params=params, headers=headers)
        time.sleep(1)
        select = Selector(response.text)
        s_x = select.xpath
        data1,data2,item_urls = read_file(filename1,filename2)
        urls = [ 'https://www.workaway.info' + _ for _ in select.xpath('//a[@class="listentry-title"]/@href').getall()]
        for url in urls:
            if url in item_urls:
                print(f'正在爬取第{page}页，检查是否有更新。{url}')
                data1,data2 = modify_one_data(url,data1,data2)
            else:
                print(f'正在爬取第{page}页，追加新数据。{url}')
                item1,item2 = get_one_data(url)
                append_to_json(filename1, item1)
                append_to_json(filename2, item2)
                data1,data2,item_urls = read_file(filename1,filename2)
  
# 保存文件名  
filename1 = 'host_profile_pairing.json'        
filename2 = 'host_profile.json'
while True:
    userinput = input('请输入对应的数字\n1：爬取数据(第一次爬取使用这个)\n2：更新数据(同时也会爬取新的数据)\n')
    if userinput == '1':
        first_get()
        break
    elif userinput == '2':
        modify_file()
        break
    else:
        print('只能输入1、2')
