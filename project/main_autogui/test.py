
import cp_image_processing
# import time


# time.sleep(3)
# cp_image_processing.haveflower()



# # 定时器测试

# import sched
# import time
# from datetime import datetime
# # 初始化sched模块的scheduler类
# # 第一个参数是一个可以返回时间戳的函数，第二参数可以在定时未到达之前阻塞
# schedule = sched.scheduler(time.time, time.sleep)
# # 被周期性调度触发函数
# def printTime(inc):
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     # schedule.enter(inc, 0, printTime, (inc,))
# # 默认参数60s
# def main(inc=60):
#     # enter四个参数分别为：间隔事件,优先级（用于同时到达两个事件同时执行的顺序），被调度触发的函数
#     # 给该触发器函数的参数（tuple形式）
#     schedule.enter(0, 0, printTime, (inc,))
#     schedule.run()
# # 5秒输出一次

# main(5)

import pyautogui
import time

flower = pyautogui.position()
deviation = (flower.x,flower.y-100)
print (flower)
print (deviation)

for i in range(1,5):
    pyautogui.moveTo(flower,duration=0.2)
    time.sleep(1)
    pyautogui.moveTo(deviation,duration=0.2)
    time.sleep(1)

# pyautogui.moveTo(flower,duration=0.5)
# pyautogui.click(button='right')
# time,sleep(1)