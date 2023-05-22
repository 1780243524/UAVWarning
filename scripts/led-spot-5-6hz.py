import time
import random
from rpi_ws281x import Adafruit_NeoPixel, Color
import os

# LED 配置:
from typing import List

LED_COUNT = 450  # 要控制LED的数量.
LED_PIN = 18  # GPIO接口 (PWM编码).
LED_BRIGHTNESS = 255  # 设置LED亮度 (0-255)
# 以下LED配置无需修改
LED_FREQ_HZ = 800000  # LED信号频率（以赫兹为单位）（通常为800khz）
LED_DMA = 10  # 用于生成信号的DMA通道（尝试5）
LED_INVERT = False  # 反转信号（使用NPN晶体管电平移位时）

# 创建NeoPixel对象
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# 初始化库
strip.begin()
with open("process", "w") as f:
    f.write(str(os.getpid()))
# 设置整体亮度 关闭LED为0 最亮为255 范围0-255
# 该函数与下面的设置颜色都不会直接对LED进行修改，可以理解为将修改数据保存到缓存区。
# strip.setBrightness(200)


# numPixels()函数介绍：取NeoPixel对象创建时设置的LED数量
for i in range(0, strip.numPixels()):  # 设置个循环(循环次数为LED数量)

    # setPixelColor()函数介绍：设置LED色值(RGB).
    # 参数1：LED 的ID (从0开始, 比如第5个LED)
    # 参数2：RGB色值  Color()RGB转Color值，参数依次为R,G,B
    # 例子：设置第5个LED颜色为红色
    #       strip.setPixelColor(4, Color(255,0,0))
    # 该函数不会直接对LED进行修改，可以理解为将修改数据保存到缓存区。
    strip.setPixelColor(i, Color(0, 0, 0))

# 提交缓存区的修改数据到WS2812B，以显示效果
strip.show()
#time.sleep(5)
count = 0
time_count = 0
right1 = list(range(0, 15))
right2 = list(range(45, 60))
right3 = list(range(60, 75))
right4 = list(range(105, 120))
right5 = list(range(120, 135))
right6 = list(range(165, 180))
right7 = list(range(180, 195))
right8 = list(range(225, 240))
right9 = list(range(240, 255))
right10 = list(range(285, 300))
right11 = list(range(300, 315))
right12 = list(range(345, 360))
right13 = list(range(360, 375))
right14 = list(range(405, 420))
right15 = list(range(420, 435))
right_all = right1 + right2 + right3 + right4 + right5 + right6 + right7 + right8 + right9 + right10 + right11 + right12 + right13 + right14 + right15

left1 = list(range(15, 30))
left2 = list(range(30, 45))
left3 = list(range(75, 90))
left4 = list(range(90, 105))
left5 = list(range(135, 150))
left6 = list(range(150, 165))
left7 = list(range(195, 210))
left8 = list(range(210, 225))
left9 = list(range(255, 270))
left10 = list(range(270, 285))
left11 = list(range(315, 330))
left12 = list(range(330, 345))
left13 = list(range(375, 390))
left14 = list(range(390, 405))
left15 = list(range(435, 450))
left_all = left1 + left2 + left3 + left4 + left5 + left6 + left7 + left8 + left9 + left10 + left11 + left12 + left13 + left14 + left15

while time_count < 300:
    if count == 0:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
    # for i in range(48,56):   #设置个循环(循环次数为LED数量)
    # strip.setPixelColor(i, Color(0,255,0))
    elif count == 6 or count == 18:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
    elif count == 5 or count == 15 or count == 25:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
    elif count == 12 or count == 24:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
    elif count == 10 or count == 20 or count == 30:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
    elif count == 36 or count == 48:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
    elif count == 35 or count == 45 or count == 55:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
    elif count == 40 or count == 50:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
    elif count == 42 or count == 54:
        for i in left_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(0, 0, 0))
        for i in right_all:  # 设置个循环(循环次数为LED数量)
            strip.setPixelColor(i, Color(255, 0, 0))
    # for i in range(30,38):   #设置个循环(循环次数为LED数量)
    # strip.setPixelColor(i, Color(255,0,0))
    strip.show()
    time.sleep(1 / 35)
    time_count = time_count + 1
    count = (count + 1) % 60
