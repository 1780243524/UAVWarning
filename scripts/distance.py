import sys
import time
import random
import os
import numpy as np

from sklearn import linear_model        #表示，可以调用sklearn中的linear_model模块进行线性回归。
import numpy as np
import sklearn.model_selection as ms
from sklearn.preprocessing import  PolynomialFeatures

#-----RSSI---------------------
# 读取文件
# i = 0
# flag = 0
# file = open(filepath)
# for line in file:
#     field = line.strip().split()
#     second = float(field[0])
#     if (field[1] != '0'):
#         data[flag].append(field[1])
#     if (second > 4.0):
#         flag = 2
#     elif (second > 2.0):
#         flag = 1
# avg = 0
# for i_sum in range(3):
#     # 计算均值
#     sum = 0
#     for i in range(len(data[i_sum])):
#         sum += int(data[i_sum][i])
#     sum /= len(data[i_sum])
#     avg += round(sum, 3)
#
# avg /= 3


#-----------阈值检测

def RSSI(rssi):
    # 5m各个距离的阈值
    threshold1 = 40
    threshold2 = 42
    threshold3 = 45
    threshold4 = 46
    threshold5 = 50

    X = [ [threshold2], [threshold3], [threshold4], [threshold5]]
    y = [ [2], [3], [4], [5]]

    #指数回归
    expmodel = linear_model.LinearRegression()
    expmodel.fit(X, np.log(y))

    return np.exp(expmodel.predict([[rssi]]))


def getDistance(arr, rssi):
    # 5m各个距离的阈值
    #threshold1 = 30.1957
    threshold2 = 20.2107
    threshold3 = 11.3553
    threshold4 = 9.781932
    threshold5 = 8.3309
    threshold7 = 7.59318
    threshold10 = 5.90214

    threshold2 = 20.2107
    threshold3 = 11.3553
    threshold4 = 10.5
    threshold5 = 9.675067
    threshold7 = 7.59318
    threshold10 = 5.90214

    X = [[threshold2], [threshold3], [threshold4], [threshold5], [threshold7], [threshold10]]
    y = [[2], [3], [4], [5], [7], [10]]

    for i in range(len(X)):
        X[i][0] -= 1

    logmodel = linear_model.LinearRegression()
    logmodel.fit(np.log(X), y)


    # 指数回归参数
    A = logmodel.intercept_ # 截距
    B = logmodel.coef_      # 线性模型的系数

    #print(A, B)

    avg = np.average(arr) - 1
    avg = np.log(avg)

    Distence = logmodel.predict([[avg]])

    # avg = np.average(arr)
    # Distence = A * np.exp(B * avg)



    if(Distence < 0):
        Distence = random.uniform(0, 0.5)
    #elif(Distence > 10):
    #    Distence = RSSI(rssi)

    return Distence




#print(getDistance(1.2, 55))

