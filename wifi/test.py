from pywifi import const, PyWiFi, Profile
import time

# wifi类
class wifi(object):
	def __init__(self):
		self.wifi = PyWiFi()									#创建一个无线对象
		self.interfaces = self.wifi.interfaces()				#获取无线网卡接口
		self.iface = self.interfaces[0]							#获取第一个无线网卡接口

	# 获取无线网卡接口
	def get_wifi_interfaces(self):
		num = len(self.interfaces)
		if num <= 0:
			print(u'未找到无线网卡接口!\n')
			exit()
		if num == 1:
			print(u'无线网卡接口: %s\n' % (self.iface.name()))
			return self.iface
		else:
			print('%-4s   %s\n'%(u'序号',u'网卡接口名称'))
			for i, w in enumerate(self.interfaces):
				print('%-4s   %s' % (i, w.name()))
			while True:
				iface_no = input('请选择网卡接口序号：'.decode('utf-8').encode('gbk'))
				no = int(iface_no)
				if no >= 0 and no < num:
					return self.interfaces[no]

	# 查看无线网卡是否处于连接状态
	def check_interfaces(self):								
		if self.iface.status() in [const.IFACE_CONNECTED, const.IFACE_CONNECTING]:
			print('无线网卡：%s 已连接。' % self.iface.name())
		else:
			print('无线网卡：%s 未连接。' % self.iface.name())

	# 扫描周围wifi
	def scan_wifi(self):
		self.iface.scan()										#扫描周围wifi
		time.sleep(1)											#不缓冲显示不出来
		result = self.iface.scan_results()						#获取扫描结果，wifi可能会有重复
		has = []												#初始化已扫描到的wifi
		wifi_list = []											#初始化扫描结果
		for i in result:
			if i not in has:									#若has中没有该wifi，则
				has.append(i)									#添加到has列表
				if i.signal > -90:								#信号强度<-90的wifi几乎连不上
					wifi_list.append((i.ssid, i.signal))		#添加到wifi列表
					print('wifi信号强度：{0}，名称：{1}。'.format(i.signal, i.ssid))#输出wifi名称
		return sorted(wifi_list, key=lambda x:x[1], reverse=True)	#按信号强度由高到低排序

	# 连接wifi
	def connect_wifi(self, wifi_name, wifi_password):
		self.iface.disconnect()									#断开无线网卡连接
		time.sleep(1)											#缓冲1秒
		profile_info = Profile()								#wifi配置文件
		profile_info.ssid = wifi_name 							#wifi名称
		profile_info.auth = const.AUTH_ALG_OPEN 				#需要密码
		profile_info.akm.append(const.AKM_TYPE_WPA2PSK)			#加密类型
		profile_info.cipher = const.CIPHER_TYPE_CCMP 			#加密单元
		profile_info.key = wifi_password 						#wifi密码
		self.iface.remove_all_network_profiles()				#删除其他配置文件
		tmp_profile = self.iface.add_network_profile(profile_info) 	#加载配置文件
		self.iface.connect(tmp_profile)							#连接
		#尝试5秒是否能成功连接(时间过短可能会导致正确密码尚未连接成功)
		time.sleep(5)				
		if self.iface.status() == const.IFACE_CONNECTED:
			print('\n==========================================================================')
			print('wifi：{0}连接成功，密码：{1}'.format(wifi_name, wifi_password), end='')
			print('==========================================================================\n')
			return True
		else:
			print('密码错误：{0}'.format(wifi_password), end='')
			return False

	# 断开无线网卡已连接状态
	def disconnect_wifi(self):
		self.iface.disconnect()					
		if self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
			print('无线网卡：%s 已断开。' % self.iface.name())
		else:
			print('无线网卡：%s 未断开。' % self.iface.name())

if __name__ == '__main__':
	wifi = wifi()												#实例化wifi类
	wifi.get_wifi_interfaces()									#获取网卡接口
	wifi.check_interfaces()										#检测网卡连接状态
	print('\n正在扫描wifi热点...')
	wifiList = wifi.scan_wifi()									#扫描周围wifi

	# wifi.disconnect_wifi()										#断开无线网卡已连接状态
