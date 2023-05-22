import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.fftpack import fft

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
    return Pyy
    #return max(Pyy[19], Pyy[20], Pyy[21])
    #index=6*N//fs
    #return max(Pyy[index], Pyy[index+1])

x = [float(l.split()[0]) for l in open("./tmp/rssi")]
y = [float(l.split()[1]) for l in open("./tmp/rssi")]
x1 = [0] * len(x)
y1 = [0] * len(y)

j = 0
for i in range(0, len(x)):
    if(y[i]):
        x1[j] = x[i]
        y1[j] = y[i]
        j += 1
x_result = x1[:j]
y_result = y1[:j]
    
#print(myFFT(y, j))
axes = plt.gca()
axes.set_ylim([0, -70])
plt.plot(x_result, y_result)
#plt.show()
now = time.localtime()
nowstr = time.strftime("-%Y-%m-%d-%H-%M")
plt.savefig("./rssiResult/rssi" + nowstr + ".png")
