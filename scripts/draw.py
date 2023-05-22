#coding:utf-8
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn
import sys

def myFFT(x):
    y = x
    PH2 = fft(y, N)  # 快速傅里叶变换

    # 下面是幅值修正
    P2 = (PH2 / N)
    P1 = P2[0:N // 2]
    P1[1:len(P1) - 2] = 2 * P1[1:len(P1) - 2]

    # PSD功率谱密度
    y = PH2
    yreal = y.real
    yimag = y.imag
    Pyy = [0] * N
    for i in range(N):
        Pyy[i] = yreal[i] * yreal[i] + yimag[i] * yimag[i]
#    return max(Pyy[19], Pyy[20], Pyy[21])
    return Pyy[29]

def FFT(x):
    y = x
    PH2 = fft(y, N)  # 快速傅里叶变换

    # 下面是幅值修正
    P2 = (PH2 / N)
    P1 = P2[0:N // 2]
    P1[1:len(P1) - 2] = 2 * P1[1:len(P1) - 2]

    # PSD功率谱密度
    y = PH2
    yreal = y.real
    yimag = y.imag
    Pyy = [0] * N
    for i in range(N):
        Pyy[i] = yreal[i] * yreal[i] + yimag[i] * yimag[i]
    return Pyy
#    return max(Pyy[19], Pyy[20], Pyy[21])

##下面是需要设定的一些数据
dataPoint=int(sys.argv[1]) #总数据点数
roundtimes= dataPoint // 300 #轮数

# 存储结果的数组
result=[0]*roundtimes

## 存储数据用数组
data=[0]*dataPoint
rssi = [0] * dataPoint
data_forward=[0]*150
data_back=[0]*150

#傅里叶变换参数
fs=30 #采样频率
N=150 #采样点数
dt=1/fs #时间间隔

#读取文件
i=0
file=open('aggregation.txt')
for line in file:
    if(i>=dataPoint):
        break
    field = line.strip().split()
    data[i]=field[2]
    i=i+1

# 读取rssi文件
i = 0
file=open("rssi")
for line in file:
    if(i >= dataPoint):
        break
    field = line.strip().split()[1].split(',')[0]
    rssi[i]= field
    i += 1

#对每一轮进行变换
for i_round in range(0, roundtimes):
    data_forward=data[i_round*330:i_round*330+150]
    data_back=data[i_round*330+180:i_round*330+330]
    #result[i_round]=myFFT(data_forward) / myFFT(data_back)
    #round(myFFT(data_forward),2)
    result[i_round]=round(myFFT(data_back)/myFFT(data_forward), 2)

#画图
if roundtimes > 1:
    x=list(range(0,roundtimes))
    plt.plot(x, result)
    for a, b in zip(x, result):
        plt.text(a, b, (a,b), ha='center', va='bottom', fontsize=5)
    plt.title('value=blink/stay')
    plt.xlabel('round')
    plt.ylabel('stay/blink')
    plt.show()
for item in result:
    print(item)

if 1:
    rssi_result = FFT(rssi)
    x=range(0,len(rssi_result))
    plt.plot(x, rssi_result)
    #for a, b in zip(x, rssi):
    #    plt.text(a, b, (a,b), ha='center', va='bottom', fontsize=5)
    plt.title('RSSI FFT VALUE')
    plt.xlabel('Hz')
    plt.ylabel('times')
    plt.show()
