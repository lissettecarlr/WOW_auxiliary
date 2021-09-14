# 说明
这儿是对python开源的一些ble代码的使用体验

# bluepy
[代码仓库](https://github.com/IanHarvey/bluepy)
该工具只能在linux上使用。
安装
```
sudo apt-get install python-pip libglib2.0-dev
sudo pip install bluepy
```
# bleak
[代码仓库](https://github.com/hbldh/bleak)
安装
```
pip install bleak
```

# pygatt

[代码仓库](https://github.com/peplin/pygatt)

该代码目前只能在linux上使用，由于手中的蓝牙适配器不支持它，在window上搜索不出来，所以只能使用linux的接口来获取蓝牙。
安装
```
pip install pygatt
pip install pyqt5
```

使用，如果提升还缺少什么包，就自行安装即可
```
python3 ble_pygatt_main.py
```

# 其他
UUID示例

0000f100-0000-1000-8000-00805f9b34fb (Handle: 21): Vendor specific
0000fff0-0000-1000-8000-00805f9b34fb (Handle: 29): Vendor specific
0000f200-0000-1000-8000-00805f9b34fb (Handle: 37): Vendor specific

mac地址示例
"54:B7:E5:79:F4:49"

pyuic5 -o ble_ui.py .\ble.ui

