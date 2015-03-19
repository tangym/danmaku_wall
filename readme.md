## 部署
和弹幕审核程序[danmaku_exam](https://github.com/tym1060326/danmaku_exam)使用环境完全相同。


### windows
- 安装[chocolatey](https://chocolatey.org/)
- 安装python3环境
```bash
choco install python
```
- 安装pip包管理器
```bash
choco install pip
```
- 安装依赖库requests
```bash
pip install requests
```
- 安装依赖库PyQt4
~下载[SIP](http://jaist.dl.sourceforge.net/project/pyqt/sip/sip-4.16.6/sip-4.16.6.zip)，并解压~（太麻烦了）
根据python版本和操作系统版本选择相应下载Non-official的[PyQt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)，打开命令行切换到下载目录下
```bash
pip install PyQt4-*.whl
```
- 检查环境配置是否成功
```bash
python --version
```
应显示`python 3.x.x`版本号
```bash
pip freeze
```
应显示
```bash
PyQt4==4.x.x
requests==x.x.x
```
- 运行程序
```bash
python danmaku_exam_gui.py
```


### ubuntu
- 安装python3环境
```bash
sudo apt-cache update
sudo apt-get install python3
```

- 使用pip安装依赖库
```bash
sudo apt-get install pip3
pip3 install requirements.txt
```

- 运行`danmaku_exam_gui.py`
```bash
python3 danmaku_exam_gui.py
```


## 功能
仿照人人墙展示弹幕。需要配合服务器端程序[gdanmaku-server](https://github.com/tuna/gdanmaku-server)使用。
程序会自动生成客户端的uuid，输入频道和播放密码，连接频道后自动全屏播放。
弹幕墙每隔3秒（可配置）刷新一次，如果有新弹幕则向上滚动显示新弹幕，否则停止滚动。
也可以使用快捷键回车控制刷新，快捷键Esc退出程序。
字体大小会根据弹幕字数自动调整，但在某些特殊情况下仍然有可能会出现弹幕无法完全显示。

## 文件说明
- `danmaku_wall_gui.py`主程序文件，负责显示窗体和驱动其余模块
- `config.py`配置文件，记录弹幕服务器的url以及刷新间隔等常量
- `channel.py`频道类文件，封装获取弹幕的接口
- `shorten_id.py`uuid生成模块，根据时间和mac地址计算一个重复率低的客户端短ID
