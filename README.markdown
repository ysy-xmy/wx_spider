# **微信公众号文章爬虫---python**
## <font color='yellow'>阐述：</font>
### 调用微信公众平台的一个接口，来获取任意公众号的文章，需要自备一个个人公众号账号，由于微信公众平台的账号密码也需要扫描登录，所以无法写成自动获取token的操作
## <font color='yellow'>功能：</font>
### 爬取公众公众号文章，支持爬取多个公众号，在setting.py文件中配置即可，
### 注意：*在使用本脚本的前提是有自己的一个订阅号，能登录到微信公众平台获取对应的cookies和token参数*
## <font color='yellow'>使用说明：</font>
### 1.首先在要在setting中进行配置，填写对应的参数，
#### wxgeturl_cookies：
获取方式如下：登录微信公众平台，新建图文
![img.png](img.png)
#### wx_token：微信公众平台的一个token，需要手动登录微信公众平台获取
![img_1.png](img_1.png)
#### wechat_accounts_name：要爬取微信公众号的名称（全称，并且完整正确）
#### passagenum:每一个公众号爬取文章的数量，例如：3，代表爬取最新的三篇文章
#### proxies:设置请求的代理地址
### 2.配置好后运行main.py