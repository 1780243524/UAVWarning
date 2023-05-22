import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn
from scipy.signal import find_peaks
import sys
import time
#def peekDect(arr, hz):
#
#    threhold=3
#    point=int(hz*N*2//fs-1)
#    indexlen=int(0.06 * N // fs)
#    leftPoint=int((hz-0.3)*2*N//fs-1)
#    rightPoint=int((hz+0.3)*2*N/fs-1)
#    peek=0
#    for i_index in range(point-indexlen, point+indexlen+1):
#        peek+=arr[i_index]
#
#    peek/=(2*indexlen+1)
#    if(peek > threhold*arr[leftPoint] and peek > threhold*arr[rightPoint]):
#        return 1
#    else:
#        return 0
N = 0
def peekDect(arr, hz):
    global N
    fs = 80
    point = int(hz * N // fs - 1)
    indexlen = int(0.2 * N // fs) + 1
    #print(point, indexlen)
    maxIndex = N // fs - 1
    for i in range(N // fs - 1, len(arr) // 2):
        if(arr[maxIndex] < arr[i]):
            maxIndex = i
    #print(maxIndex)
    if (maxIndex >= point - indexlen and maxIndex <= point + indexlen):
        return 1
    return 0



def judgeDetect():
    #傅里叶变换参数
    fs = 80 #采样频率
#   N = int(sys.argv[1])#采样点数
    dt = 1/fs #时间间隔

    #读取文件
    data = []
    file = open('./tmp/aggregation80.txt')
    for line in file:
        field = line.strip().split()
        if field:
            data.append(field[2])
    if len(data) < 14:
        return "it is not fpv"
    else:
        global N
        N = len(data)
        y = data
        PH2 = fft(y, N) #快速傅里叶变换
        #下面是幅值修正
        P2 = (PH2/N)
        P1 = P2[0:N//2]
        P1[1:len(P1)-2] = 2 * P1[1:len(P1)-2]

        #PSD功率谱密度
        y = PH2
        yreal = y.real
        yimag = y.imag
        Pyy = [0]*N
        for i in range(N):
            Pyy[i] = yreal[i] * yreal[i] + yimag[i] * yimag[i]
        if(peekDect(Pyy, 24) or peekDect(Pyy, 25) or peekDect(Pyy, 30)):
            return "it is fpv!"
        else:
            return "it is not fpv"


    #画图
    '''f=list(range(1,N//2))
    f=[i*fs/N for i in f]
    #plt.rcParams['font.sans-serif']=['SimHei']#显示中文标签
    #plt.rcParams['axes.unicode_minus']=False
    plt.subplot(211)
    plt.plot(f, abs(P1[1:N//2]))
    #plt.title(u'时域信号')
    plt.xlabel('f(Hz)')
    plt.ylabel('|P1(f)|')


    plt.subplot(212)
    plt.plot(f, Pyy[1:N//2])
    #plt.title(u'功率谱密度')
    plt.xlabel('f(Hz)')
    plt.ylabel('|P1(f)|^2')
    #plt.show()
    now = time.localtime()
    nowstr = time.strftime("-%Y-%m-%d-%H-%M")
    plt.savefig("./fpvResult/fpv" + nowstr + ".png")
'''
