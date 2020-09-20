# -*- coding: utf-8 -*-
from requests import get, Session
from config import USERNAME, PASSWORD, CATEGORY_NAME, LANGUAGE, PROJECT, CMNAMESPACE, CMLIMIT

def login():
    '''
    帳號登入
    '''
    S = Session()
    PARAMS_0 = {"action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json"}
    R = S.get(url=api_url, params=PARAMS_0)
    DATA = R.json()
    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
    
    PARAMS_1 = {"action": "clientlogin",
                "username": USERNAME,
                "password": PASSWORD,
                "loginreturnurl":'http://127.0.0.1:5000/',
                "logintoken": LOGIN_TOKEN,
                "format": "json"}

    R = S.post(api_url, data=PARAMS_1)
    DATA = R.json()
    print('{}\n使用者名稱：{}\n登入狀態：{}\n{}'
          .format('========================================',
                  DATA['clientlogin']['username'],
                  DATA['clientlogin']['status'],
                  '========================================'))
    return [S,DATA['clientlogin']['status']]

def editor(title,text,summary='null edit',minor=True):
    '''
    執行零編輯
    '''
    PARAMS_2 = {"action": "query",
                "meta": "tokens",
                "format": "json"}
    R = S.get(url=api_url, params=PARAMS_2)
    DATA = R.json()
    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
    PARAMS_3 = {"action": "edit",
                "title": title,
                "token": CSRF_TOKEN,
                "format": "json",
                "text": text,
                'minor': minor,
                "summary": summary}
    R = S.post(api_url, data=PARAMS_3)
    DATA = R.json()
    return DATA

def get_pages_in_category():
    '''
    獲取分類中的頁面
    '''
    response = get('https://{}.{}.org/w/api.php'.format(LANGUAGE,PROJECT),
                   params= {"action": "query",
                            "format": "json",
                            "list": "categorymembers",
                            "cmtitle":CATEGORY_NAME, #分類名稱
                            "cmlimit": CMLIMIT, #搜索上限
                            "cmnamespace":CMNAMESPACE #命名空間
                            }).json()
    title = [member['title'] for member in response['query']['categorymembers']]
    return title

def get_wikitext(title):
    '''
    抓取頁面中的Wikitext
    '''
    response = get('https://{}.{}.org/w/api.php'.format(LANGUAGE,PROJECT),
                    params={"action": "query",
                            "format": "json",
                            "titles": title,
                            "prop": "revisions",
                            "rvprop": "content",
                            }).json()
    page = next(iter(response['query']['pages'].values()))
    article_text = page['revisions'][0]['*']
    return article_text

if __name__ == '__main__':
    api_url = 'https://{}.{}.org/w/api.php'.format(LANGUAGE,PROJECT)
    try:
        logins = login()
        S = logins[0]
        if logins[1] == 'PASS': #成功登入則執行
            categories = get_pages_in_category()
            print('目標分類「',LANGUAGE,':',CATEGORY_NAME,'」計',str(len(categories)),'個頁面',sep='',end=' ')
            print('正在執行零編輯...')
            try:
                status=[]
                for cat in range(len(categories)):
                    wikitext = get_wikitext(title=categories[cat])+'{{subst:void}}'
                    status.append(editor(title=categories[cat],text=wikitext))
                    print('\r','已完成{}/{} ({:.2%})'.format(cat+1,len(categories),((cat+1)/len(categories))),end='', flush=True)
                print('\n執行完成。')
            except:
                print('Error: 程序執行失敗！請檢查您所輸入之設定值是否有誤。') 
        else:
            print('Error: 登入失敗！請稍後再登入。')
    except:
        print('Error: 登入失敗！請檢查您的帳號或密碼是否輸入正確。')
