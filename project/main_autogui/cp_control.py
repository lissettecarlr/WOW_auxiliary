# 用于存放一些游戏中的通用操作

import pyautogui
import time
import pyscreeze


ccfd = 0.6
# 自动小退函数 默认进行5次尝试，成功返回Ture
def return_login_screen():
    #输入小退命令
    print("start")
    # time.sleep(2)
# 该方式需要先确认是否打开了输入法   
    # pyautogui.press('enter')
    # pyautogui.typewrite('/camp', interval=0.01) 
    # pyautogui.press('enter')
# 鼠标点击方式 请不要移动
    test=5
    while(test>0):
        pyautogui.press('esc')
        # 寻找小退按键
        try:
            ret_button=pyautogui.locateOnScreen('./pic/key_return_login.PNG',confidence=ccfd)
            target=pyautogui.center(ret_button) 
            break
        except:
            test=test-1
            print("not find,test=%d",test)
            continue
    if(test>0):
        pyautogui.moveTo(target,duration=0.5)
        pyautogui.click(button='left')
        return True
    else:
        return False


# 从角色选择界面点击进入游戏
def enter_login():
    print("start")
    test=5
    while(test>0):
        try:
            ret_button=pyautogui.locateOnScreen('./pic/key_login.PNG',confidence=ccfd)
            target=pyautogui.center(ret_button) 
            break
        except:
            test=test-1
            print("not find,tset=%d",test)
            continue
    if(test>0):
        pyautogui.moveTo(target,duration=0.5)
        pyautogui.click(button='left')
        return True
    else:
        return False


