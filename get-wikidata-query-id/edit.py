# -*- coding: utf-8 -*-
import re
import numpy as np
from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame as df
from config import category_name, language, project, exclude

def get_pages_in_category(category_name,language,project,exclude): 
    '''
    獲取分類中的頁面
    '''
    print('正在獲取「',language,':',category_name,'」中的頁面...',sep='')
    data=[]
    data_string=[]
    web_url = "https://"+language+"."+project+".org/wiki/"+category_name
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
               'AppleWebKit/537.36 (KHTML, like Gecko)'
               'Chrome/81.0.4044.138 Safari/537.36',}
    try:       
        for x in BeautifulSoup(get(web_url,headers=headers).text,'lxml').find_all(["div"], class_="mw-category-generated"):
            data.extend(x.find_all("a", href=re.compile(exclude), class_="", accesskey=""))
        for y in range(len(data)):
            data_string.append(data[y].string.encode('utf-8').decode('utf-8'))
        print(' 獲取完成：共計',str(len(data_string)),'個頁面。',sep='')
    except:
        data_string='ERROR: 請檢查您所輸入之參數是否有誤。'
    return data_string

def get_qid(pagename,language,project):
    '''
    透過API獲取頁面之Qid
    '''
    try:
        response = get(
         'https://'+language+'.'+project+'.org/w/api.php',
        params={
             'action': 'query',
             'format': 'json',
             'titles': pagename,
             'prop': 'pageprops',
             'rvprop': 'content',
         }).json()
        pageid = next(iter(response['query']['pages'].values()))
        qid = pageid['pageprops']['wikibase_item']
    except:
        qid= np.nan #若無Qid則填空值   
    return qid

def results(category_name,language,project,exclude):
    '''
    獲取結果並輸出
    '''
    pages = get_pages_in_category(category_name,language,project,exclude)
    pages_qid=[]
    print('正在透過API獲取頁面之Qid')
    for p in range(len(pages)):
        pages_qid.append(get_qid(pages[p],language,project))
        print('\r','已完成',str(p+1)+'/'+str(len(pages)),'({:.2%})'.format((p+1)/len(pages)),end='', flush=True)
    dataframes = df(dict(qid=pages_qid,page=pages))
    with open('result.csv','w+',newline='') as output:
        dataframes.to_csv(output,encoding='utf-8',index=False)
        print('\n輸出完成。')

if __name__ == '__main__':
    results(category_name,language,project,exclude)
