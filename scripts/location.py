import sys
import os
import random


#flag = 0-middle,1-left, 2-right
def locate(flag = 0):
    realAngle = 30
    ret = []
    angle = 0
    distence = 3
    if(flag == 0):
        angle = 90
    elif(flag == 1):
        seed = random.randint(0,10)
        if(seed < 8):
            angle = random.randint(90 - realAngle/2 - 5 , 90 - realAngle/2
    return [distence, angle]

#print(locate(1))

