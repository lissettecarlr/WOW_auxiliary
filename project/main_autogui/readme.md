# main_autogui
该工程主要解决一下简单的点击和按键操作，通过控制面板选择不同任务执行，暂定程序名称为cp

### 相关包
pip install pyautogui
pip install PyQt5
pip install PyQt5-tools
pip install requests
pip install configparser
pip install opencv-python

封成EXE的需要
pip install future  -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pyinstaller

### 文件分类
* cp_mian_ui.py
使用pyuic5 -o cp_main_ui.py main.ui 命令转换而得，主要是界面代码

* cp_control.py
封装了autogui的各种操作命令

* cp_main.py
主逻辑，启动交互界面，执行选择的任务

* cp_dragon_buff.py
子任务，当检测到获取到龙头BUF后下线，并且发送通知

* cp_config.py cp_config_init
保存一些信息

* cp_communication.py
通讯相关

* cp_control.py
存放一些对游戏的常规操作，例如小退


### 目前功能

* 暴风龙头
当检测到有龙头BUF的时候小退的角色选择画面，如果设置了server酱的key则通过微信发送通知
当长时间不操作游戏自动小退的时候，该软件会自动点击进入游戏
当长时间不操作游戏自动退出到登录画面的时候，发送微信通知

使用注意:
默认的匹配用图片只适用于1920*1080的游戏分辨率，如果是其他分辨率请自行截图按照pic里面的说明替换
游戏请作为最上级窗体，操作是模拟鼠标和键盘。

* 哈卡
逻辑和使用方式和龙头相同

* 风歌花
暂定逻辑:
从角色选择画面开始，启动任务后弹出输入框，设定自动上线定时。
上线后识别风歌花(当未识别到风歌花图标则发送微信通知)，鼠标移动其上，右键单击，鼠标向上移动固件距离，再次返回单击，重复，如果是在未识别到风歌花图标的情况下，则以当前鼠标位置作为风歌花位置，也就是说可以人为手动移动到风歌花上
当检测到风歌花buf图标则小退，如果超过4分钟未获取到风歌花则也小退，两种情况均发生微信通知

