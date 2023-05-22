#coding:utf-8
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn
import sys
import time
import random


'''filename = './tmp/res.txt'
with open(filename, 'w') as file_object:
    file_object.write(str(y_predict[0]) + " " + str(gredit))'''

#coding:utf-8
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn
def airspot():
    #傅里叶变换参数
    fs=30 #采样频率
    N=300 #采样点数
    dt=1/fs #时间间隔
    
    dataPoint=150 #总数据点数
    
    #读取文件
    i=0
    data=[0]*N
    file=open('./tmp/aggregation.txt')
    for line in file:
        if(i >= dataPoint):
            break
        field = line.strip().split()
        data[i]=field[2]
        i=i+1

    y=data[0:150]
    PH2=fft(y, N)                     #快速傅里叶变换
    
    #下面是幅值修正
    P2=(PH2/N)
    P1=P2[0:N//2]
    P1[1:len(P1)-2]=2*P1[1:len(P1)-2]



    #PSD功率谱密度
    y=PH2
    yreal=y.real
    yimag=y.imag
    Pyy=[0]*N
    for i in range(N):
        Pyy[i]=yreal[i]*yreal[i]+yimag[i]*yimag[i]

    #求各个区间均值
    interval_avg = [0] * 6;
    for i in range(6):
        for j in range(5):
            interval_avg[i] = interval_avg[i] + Pyy[40 + i * 5 + j]
        interval_avg[i] = interval_avg[i] / 5

    min = np.min(interval_avg)
    
    interval = 6 * [0]
    for i in range(6):
        interval[i] = interval_avg[i] / min
    r = 0
    for i in range(6):
        r = r + (interval[3] - interval[i])
    r = r / interval[3]
    return [str(round(r,3)), interval[3]]


'''filename = './tmp/res.txt'
with open(filename, 'w') as file_object:
    file_object.write(str(round(r, 3)))'''






