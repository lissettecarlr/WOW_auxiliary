# 屏幕抓取
import time
from PIL import ImageGrab
from PIL import Image, ImageDraw, ImageFilter

def grab_test():
    print("start!")

    ###############################################
    # 全屏抓取
    ImageGrab.grab().save(".\out\img_test.png")

    ###############################################
    # 指定范围抓取
    # img = ImageGrab.grab(bbox=(100, 10, 200, 200))
    # img.save(".\out\img_capture_clip.png")

def filte_draw_test():
    im_rgb = Image.open('pic/pic_1.png')
    ###############################################
    # 半透明50%(128/255)
    # im_rgba = im_rgb.copy()
    # im_rgba.putalpha(128)
    # im_rgba.save('out/img_putalpha.png')

    ###############################################
    # 切出形状透明
    im_a = Image.new("L", im_rgb.size, 255) # white
    #生成一个画笔
    draw = ImageDraw.Draw(im_a)
    #涂抹出一个指定区域为黑其他区域为白的图片
    draw.rectangle((200, 100, 300, 200), fill=0, outline=0) # black
    # draw.ellipse((200, 100, 300, 200), fill=0)
    im_a.save("out/img_a.png")
    im_rgba = im_rgb.copy()
    #将生产的图片传入作为滤镜，将会过滤掉黑色部分
    im_rgba.putalpha(im_a)
    # 高斯羽化 Start
    # im_a_blur = im_a.filter(ImageFilter.GaussianBlur(1))
    # im_rgba.putalpha(im_a_blur)
    # 高斯羽化 End

    im_rgba.save('out/img_putalpha.png')


filte_draw_test()