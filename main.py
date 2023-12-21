import time
import requests
import json
import warnings
warnings.filterwarnings("ignore")
import setting
from setting import proxies
from bs4 import BeautifulSoup
from setting import passagenum
import json
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
}
#一个处理返回结果的函数
def dealspring(prostring):
    return json.loads(prostring["publish_page"])['publish_list']

#获取公众号文章链接
def geturl():
    wechat_accounts_fakeid={}
    for item in setting.wechat_accounts_name:
        params1 = {
            'action': 'search_biz',
            'begin': '0',
            'count': '1',
            'query': item,
            'token': setting.wx_token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        try:
            response = requests.get('https://mp.weixin.qq.com/cgi-bin/searchbiz',verify=False,
                                        params=params1, cookies=setting.wxgeturl_cookies, headers=headers, proxies=proxies)
            if json.loads(response.text)['base_resp']['ret'] == 200040:
                print('微信公众号token过期')
                return 0
            fakeid = json.loads(response.text)['list'][0]['fakeid']
            wechat_accounts_fakeid[item] = fakeid
        except requests.exceptions.ConnectionError as e:
            # 处理连接错误的异常逻辑
            print("请求断了,10秒后重试，", e)
            time.sleep(10)
            geturl()
            return 0
    #多个公众号的文章获取，每一个fakeid对应一个公众号，要爬取的公众号在seetting中配置
    for key in wechat_accounts_fakeid:
        params2 = {
            'begin': '0',
            'count': passagenum ,
            'query': '',
            'fakeid': wechat_accounts_fakeid[key],
            'type': '101_1',
            'free_publish_type': '1',
            # 'sub_action': 'list_ex',
            'token': setting.wx_token,  # 需要定时更换token
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        # print(response.text)
        try:
            response = requests.get('https://mp.weixin.qq.com/cgi-bin/appmsgpublish', verify=False,
                                    params=params2, cookies=setting.wxgeturl_cookies, headers=headers, proxies=proxies)
            # 在这里处理正常响应的逻辑
            if json.loads(response.text)=={"base_resp":{"ret":200003,"err_msg":"invalid session"}}:
                print('微信公众号token过期')
                return 0
        except requests.exceptions.ConnectionError as e:
            # 处理连接错误的异常逻辑
            print("请求断了,10秒后重试，", e)
            time.sleep(10)
            geturl()
            return 0
        passages = []#用来存每一个公众号的文章链接
        for i in range(passagenum):
            list=json.loads(dealspring(json.loads(response.text))[i]['publish_info'])['appmsg_info']
            for b in list:
             passage = list[list.index(b)]
             temp = {'title': passage['title'], 'url': passage['content_url']}
             passages.append(temp)
             # print(temp)
        response.close()
        print("目前爬取的公众号是：",key)
        for i in passages:
            # 这里加上文章链接的判断
            print(i['title'], i['url'])
            response = requests.get(i['url'], headers=headers, proxies=proxies, verify=False)
            # 在这里处理正常响应的逻辑
            soup = BeautifulSoup(response.text, 'lxml')
            onlytext = soup.text.replace(" ", "").replace("\n", "")
            print(f'从文章中提取到的文本是：{onlytext}')
            print()
            print('-----------------我是分割线😎😎😎-------------------')
            print()
        # 呼，休息一下，三秒后再获取另一个公众号的😊😊😊
        time.sleep(3)
geturl()