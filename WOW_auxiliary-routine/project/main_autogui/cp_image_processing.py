# 该文件用于识别游戏画面

import pyautogui
import time
import pyscreeze
import os



def listDir(path, list_name):
    """
    :param path: 路径
    :param list_name: path下所有文件的绝对路径名的列表
    :return:
    """
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listDir(file_path, list_name)
        else:
            list_name.append(file_path)




cfd = 0.6

#是否在角色选择画面
def isLogin():
    try:
        ret_button=pyautogui.locateOnScreen('./pic/key_login.PNG',confidence=cfd)
        target=pyautogui.center(ret_button) 
        return True
    except:
        print("not find login.PNG")
        return False

# 是否在登陆画面
def isLogout():
    try:
        ret_button=pyautogui.locateOnScreen('./pic/key_user.PNG',confidence=cfd)
        target=pyautogui.center(ret_button) 
        return True
    except:
        print("not find logout.PNG")
        return False 

# 通过背包图标判断是否在游戏界面
def isGame():
    try:
        ret_button=pyautogui.locateOnScreen('./pic/bag.PNG',confidence=cfd)
        target=pyautogui.center(ret_button) 
        return True
    except:
        print("not find bag.PNG")
        return False 


# 判断是否有龙头BUF
def haveBuffhead():
    try:
        ret_button=pyautogui.locateOnScreen('./pic/buf_dragon.PNG',confidence=cfd)
        target=pyautogui.center(ret_button) 
        return True
    except:
        print("not find head.PNG")
        return False 

# 判断是否有卡哈BUF
def haveBuffHaka():
    try:
        ret_button=pyautogui.locateOnScreen('./pic/buf_haka.PNG',confidence=cfd)
        target=pyautogui.center(ret_button) 
        return True
    except:
        print("not find head.PNG")
        return False 

# 判断是否有风歌花
def haveflower():
    # 获取所以风歌花图片依次对比
    list_name =[]
    listDir("./pic/flower",list_name)
    for p in list_name:
        try:
            ret_button=pyautogui.locateOnScreen(p,confidence=0.4)
            target=pyautogui.center(ret_button)
            #移动鼠标到该花上
            # pyautogui.moveTo(target,duration=0.5)
            return target
        except:
            print("not find:"+p)
            continue  
    
    return None

# 判断是否有风歌花BUF
def haveBuffFlower():
    try:
        ret_button=pyautogui.locateOnScreen('./pic/buf_flower.PNG',confidence=cfd)
        target=pyautogui.center(ret_button) 
        return True
    except:
        print("not find flower buf.PNG")
        return False    