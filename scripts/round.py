#coding:utf-8
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn
import sys
import time
import random

def myFFT(x, N):
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
    #return max(Pyy[19], Pyy[20], Pyy[21])
    index=6*N//fs - 1
    return max(Pyy[index], Pyy[index+1])

#傅里叶变换参数
fs=30 #采样频率
#N=blinkPoint #采样点数
dt=1/fs #时间间隔

##宏
startTime=5
startPoint=fs*startTime
duringTime=5
blinkPoint=fs*duringTime
dataPoint=300 #总数据点数

## 存储数据用数组
data=[0]*dataPoint
data_forward=[0]*startPoint
data_back=[0]*blinkPoint
value_forward=[0]*startPoint
value_back=[0]*blinkPoint
value_result = [0]*startPoint

import os
allName = os.popen("ls ./stay2/").read().split('\n')
allName = allName[:-1]
#print(allName)
sum = 0
#读取文件
for item in allName:
    i=0
    file=open('./stay2/' + item)
    for line in file:
        if(i>=dataPoint):
            break
        field = line.strip().split()
        data[i]=field[2]
        i=i+1
    i=0
    for i in range(startPoint):
        data_forward[i]=data[i]
    i=0
    for i in range(blinkPoint):
        data_back[i]=data[i+startPoint]

    base = myFFT(data_forward, startPoint)

    gredit=0
    for i_dur in range(30, blinkPoint):
        value_forward[i_dur] = myFFT(data_forward[startPoint-i_dur:startPoint], i_dur)
        value_back[i_dur] = myFFT(data_back[0:i_dur], i_dur)
        threhold=2
        #if(i_dur > 30 and value_forward[i_dur]/value_forward[i_dur-1] > threhold):
         #   value_forward[i_dur] = random.uniform(0.9, 1.5) * value_forward[i_dur - 1]
        value_result[i_dur] = value_back[i_dur] / value_forward[i_dur]
        if(value_result[i_dur] > 1 and i_dur < 90):
            if(value_result[i_dur] <= 3):
                gredit+=1
            elif(value_result[i_dur] <= 5):
                gredit+=10
            else:
                gredit+=30
#    value_result[i_dur] = value_back[i_dur] / base

#print(value_back)
#print(value_forward)

#画图
    #x=list(range(30, blinkPoint))
    #for i in range(0, len(x)):
    #    x[i] /= 30
    #ax1 = plt.subplot(211)
    #plt.plot(x, [base] * (blinkPoint - 30), color="royalblue")
    #plt.plot(x, [value_forward[30]] * (startPoint - 30), color="royalblue")
    #plt.plot(x, value_forward[30:blinkPoint], color="royalblue")
    #plt.plot(x, value_back[30:blinkPoint], color="red")
    
    #ax2 = plt.subplot(212)
    #plt.plot(x, value_result[30:blinkPoint], color="gold")
    #plt.plot(x, [1] * (blinkPoint-30), color="green")
    #plt.plot(x, [3] * (blinkPoint-30), color="green")
    #plt.plot(x, [5] * (blinkPoint-30), color="green")
    #plt.title('value')
    #plt.xlabel('duringtime')
    #plt.ylabel('fft')
    #now = time.localtime()
    #nowstr = time.strftime("-%Y-%m-%d-%H-%M")
    #plt.savefig('./fft/fft-result' + nowstr + '.png')#保存图片
    #plt.show()
    #print(gredit)


    import csv, os, sys
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC
    from sklearn.utils import check_random_state
    from sklearn import svm, datasets
    import sklearn.model_selection as ms
    import joblib

    
    #加载model，只有保存一次后才能加载model
    clf=joblib.load('./model/clf.pkl')
    y_predict = clf.predict([value_result[30: blinkPoint - 30]])
    if gredit > 100000000:
        y_predict[0] = 1
    if y_predict[0] == -1:
        y_predict[0] = 0
    print(y_predict)
    sum += y_predict
print(sum)
