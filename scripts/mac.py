import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
x = [l.split(',')[0] for l in open("mac.safe")]
y = [l.split(',') for l in open("mac")]
for item in y:
    item[1] = int(item[1])
for i in range(0, len(y)):
    if y[i][0] not in x:
        print(y[i])
