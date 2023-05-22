# function:  calc the angle of the drone
# time:      2021/7/16
# by zyg

import numpy as np
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import seaborn

from sklearn import linear_model        #表示，可以调用sklearn中的linear_model模块进行线性回归。
import numpy as np
import sklearn.model_selection as ms
from sklearn.preprocessing import  PolynomialFeatures

def getAngle():
    # 傅里叶变换参数
    fs = 30  # 采样频率
    N = 300  # 采样点数
    dt = 1 / fs  # 时间间隔

    # 读取文件
    i = 0
    data = [0] * N
    dataPoint = 300

    file = open('/home/kali/ciscn/UAVWarning/stable/tmp/aggregation.txt')
    for line in file:
        if (i >= dataPoint):
            break
        field = line.strip().split()
        data[i] = field[2]
        i = i + 1

    y = data[0:180]
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

    sum5hz = 0
    sum6hz = 0
    sumBase1 = 0
    sumBase2 = 0
    # 计算5hz均值
    for i in range(40, 45):
        sum5hz += Pyy[i]
    # 计算6hz均值
    for i in range(58, 63):
        sum6hz += Pyy[i]
    # 计算基址7-9hz，11-13hz均值
    for i in range(70, 91):
        sumBase1 += Pyy[i]
    for i in range(110, 131):
        sumBase2 += Pyy[i]

    avg5 = sum5hz / 5
    avg6 = sum6hz / 5
    avgBase = min(sumBase1, sumBase2) / 20

    snr1 = avg5 / avgBase
    snr2 = avg6 / avgBase

    # 5m各个距离的阈值
    threshold1 = 1.120992
    threshold2 = 1.423554

    X = [[threshold1], [threshold2]]
    y = [[45], [135]]

    logmodel = linear_model.LinearRegression()
    logmodel.fit(np.log(X), y)

    # 指数回归参数
    A = logmodel.intercept_  # 截距
    B = logmodel.coef_  # 线性模型的系数

    angle = logmodel.predict([[snr2 / snr1]])
    return int(angle)


#print(snr1, snr2)

# # 画图
# f = list(range(1, N // 2))
# f = [i * fs / N for i in f]
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
# plt.rcParams['axes.unicode_minus'] = False
# plt.subplot(221)
# plt.plot(f, abs(P1[1:N // 2]))
# plt.title(u'时域信号')
# plt.xlabel('f(Hz)')
# plt.ylabel('|P1(f)|')
#
# plt.subplot(222)
# plt.plot(f, Pyy[1:N // 2])
# plt.title(u'功率谱密度')
# plt.xlabel('f(Hz)')
# plt.ylabel('|P1(f)|^2')
# plt.show()
