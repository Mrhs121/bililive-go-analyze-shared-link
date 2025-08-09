from flask import Flask, request, render_template
from urllib.parse import urlparse
import sys
import re
import requests
import json

app = Flask(__name__)

if len(sys.argv) < 2:
    print("Usage：python app.py <nas_biligo_url>")
    sys.exit(1)

def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url

raw_url = sys.argv[1]
nas_biligo_url = normalize_url(raw_url).rstrip("/")
print(nas_biligo_url)
nas_biligo_post_api = nas_biligo_url + "/api/lives"


user_agent = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]

get_HEADER = {
    'User-Agent': user_agent[2],  # 浏览器头部
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 客户端能够接收的内容类型
    'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
    'Connection': 'keep-alive',  # 表示是否需要持久连接
    'Host': 'v26.douyinvod.com'
}
def get_html_text(url):
    r = requests.get(url, get_HEADER)
    r.encoding = "utf-8"
    return r.text, r.status_code


def Find(string):
    # findall() 查找匹配正则表达式的字符串
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    url = re.findall(pattern,string)
    print("live url is ", url)
    return url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/down/',methods=['post'])
def download():
    # print('request.data ',request.data)
    if not request.data:   #检测是否有数据
        print('fail')
        return 'fail'
    dy = request.data.decode('utf-8')
    shared_url = Find(str(dy))
    res = 'success'
    if len(shared_url) == 0:
        return "无效链接"
    else:
        html, code = get_html_text(str(shared_url[0]))
        matches = re.findall(r'\\"webRid\\":\\"(\d+)\\"', html)
        live_id = next((v for v in matches if v), None)
        if live_id != '':
            print(live_id)
            res = redirect_to_biligo(live_id)
    return res

def redirect_to_biligo(live_id):
    url = "https://live.douyin.com/{}".format(live_id)
    print("living room url is ", url)
    payload = json.dumps([
        {
            "url": url,
            "listen": True
        }
    ])
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': nas_biligo_url,
        'Referer': nas_biligo_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'content-type': 'application/json'
    }
    response = requests.request("POST", nas_biligo_post_api, headers=headers, data=payload)
    try:
        json_data = response.json()
        print(json_data)
    except ValueError:
        print(response.text)
    return url


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
