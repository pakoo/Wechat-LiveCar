# Wechat-LiveCar

微信直播车

通过树莓派小车 推送直播信号给服务器，同时和服务器保持长链接。

然后使用微信小程序 实时操控小车移动并返回小车摄像头画面。

延迟控制在500毫秒以内。

./
├── README.md

├── car.py           //小车控制代码

├── carclient.sh     //小车初始化服务脚本和直播推流脚本

├── livecar          //etc.d 脚本 自动启动使用

└── twss.py          //小车接收控制指令客户端

![](https://pic1.zhimg.com/80/v2-7ecfe7bad5a3c173a60604fcf9d17ac4_hd.jpg)
