# bililive-go-analyze-shared-link
bililive-go的扩展插件，直接通过手机上获取到的直播间分享链接即可解析对应的直播间号，并调用bililive-go添加直播间API自动开始录制


## 1. 安装依赖

在运行本项目前，请先安装以下 Python 库：

```
pip install flask requests
```


## 2. 启动
服务默认端口8888
```
python live_http_server.py <bililive-go 的 url>
```
例如bililive-go的url为http://192.168.6.188:8080，具体的执行命令即为：
```
python live_http_server.py 192.168.6.188:8080
```

<img width="1084" height="137" alt="截屏2025-08-09 19 25 24" src="https://github.com/user-attachments/assets/f5e533f5-3175-422a-95ab-5c2b02ca5ba8" />

### 构建Docker镜像
```
docker build -t bililive-go-analyze:latest .
```
飞牛NAS示例

```docker pull shengsheng123/bililive-go-analyze-shared-link:latest```

<img width="670" height="290" alt="截屏2025-08-09 21 16 18" src="https://github.com/user-attachments/assets/2ec99eeb-9bd6-401d-9b06-467e37b94665" />

<img width="656" height="204" alt="截屏2025-08-09 21 16 13" src="https://github.com/user-attachments/assets/72ca52ab-72f7-44b9-8bcd-bfb52e68d4b6" />


## 3. Demo 演示
例如QQ飞车手游的抖音直播间

![5c527cb0d0a3650187e494e7a176448a](https://github.com/user-attachments/assets/b7cde83b-50c2-435f-88c3-b5ba28f51315)

手机上点击分享，获取到的链接如下：
```
4- #在抖音，记录美好生活#【橘姐的好友局 8月一起肘】直播中 。复制下方链接，打开【抖音】，直接观看节目！ https://v.douyin.com/toKkW71KCGE/ 5@2.com :8pm
```
直接将该链接完整的复制到文本框中即可
![ad33372d7580a09fb3ad8dcbc68e70d6](https://github.com/user-attachments/assets/2172782d-7f7b-455d-a97a-53d851631030)
![ea9a35298eb573997bf61fdc5c5b69d7](https://github.com/user-attachments/assets/2190ab23-e30e-4999-b8bd-b03580a343c1)


<img width="1916" height="441" alt="截屏2025-08-09 19 31 35" src="https://github.com/user-attachments/assets/c6b1f97f-0c6d-4500-9c0f-6bde4b8ec896" />
完成录制
<img width="1362" height="75" alt="截屏2025-08-09 19 31 09" src="https://github.com/user-attachments/assets/74e8a0c3-f620-441e-b421-55e40edb0695" />
