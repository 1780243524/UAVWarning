import sys
import os
import time
import re
import subprocess
from multiprocessing import Process

#mac = "60:60:1f:49:2d:69"
#channel = "13"
#mac = "E6:25:CC:8D:6E:4D"
#channel = "11"
dangerMac = []
fpvMac = []
dangerMacDict = {}
def scan():
    excuteCommand("./scripts/mac.sh 3")

#def detect(mac=mac, channel=channel):
#    return excuteCommand("./scripts/detect.sh " + mac + " " + channel)

def initialize():
    excuteCommand("./scripts/mac.sh 10")

def blinkLED():
    for line in open("./tmp/mac.fpv"):
        channel = line.split(" ")[1]
        mac = line.split(" ")[0]
        print("Judging " + mac)
        excuteCommand("./scripts/tshark.sh " + mac + " blink " + channel)
        printBlank()
        with open('./tmp/res.txt', 'r') as f:
            list1 = f.read()
            list1 = list1.split(' ')
            #for i in range(0, len(list1)):
            #    list1[i] = list1[i].rstrip('\n')
            predict = "predict:" + list1[0]
            y_predict = "y_predict:" + list1[1]
            print(predict)
            print(y_predict)

def stayLED():
    for line in open("./tmp/mac.fpv"):
        channel = line.split(" ")[1]
        mac = line.split(" ")[0]
        print("Judging " + mac)
        excuteCommand("./scripts/tshark.sh " + mac + " stay " + channel) 
        printBlank()

#过滤危险MAC地址
def filter():
    x = [l.split(',')[0] for l in open("./data/mac.safe")]
    y = [l.split(',') for l in open("./tmp/mac")]
    global dangerMac
    dangerMac = []
    for item in y:
        item[1] = int(item[1])
    for i in range(0, len(y)):
        if y[i][0] not in x:
            dangerMac += y[i]
    f = open("./tmp/mac.danger", "w")
    if dangerMac:
        f = open("./tmp/mac.danger", "w")
        for i in range(0, len(dangerMac), 2):
            f.write(dangerMac[i] + " " + str(dangerMac[i + 1] ) + '\n')
    f.close()

def detect():
    global strStatus, fpvMac
    dangerMac = [l.split(' ') for l in open("./tmp/mac.danger")]
    if dangerMac:
        for item in dangerMac:
            result = excuteCommand("./scripts/detect.sh " + item[0] + " " + item[1][:-1])
            printBlank()
            print(item[0] + " -> " + result[:-1])
            if not re.search("not", result) and (fpvMac == [] or item[0] not in fpvMac):
                fpvMac += item
            else:
                if item[0] not in dangerMacDict.keys():
                    dangerMacDict[item[0]] = 1
                else:
                    dangerMacDict[item[0]] += 1
                if dangerMacDict[item[0]] > 1:
                   # print("add mac!!!")
                    with open("./data/mac.safe", "a+") as f:
                        f.write(item[0] + ", " + item[1])
        f = open("./tmp/mac.fpv", "w")
        for i in range(0, len(fpvMac), 2):
            f.write(fpvMac[i] + " " + fpvMac[i+1])
            #print(fpvMac[i] + " " + fpvMac[i+1])
        f.close()

def excuteCommand(com):
    command = ['/bin/bash'] + com.split()
    ex = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = ex.communicate()
    status = ex.wait()
    #print("cmd in ", " ".join(command))
    #print("cmd out ", out.decode())
    try:
        return out.decode()
    except:
        return "excute decode error"

def printBlank():
    print("\r\b\r\b\r\b\r\b\r\b\r\b")
    for i in range(6):
        print("                                                                       ")
    print("\r\b\r\b\r\b\r\b\r\b\r\b\r\b")

def autoProcess():
    os.popen("rm -f ./tmp/mac ./data/mac.safe ./tmp/mac.danger ./tmp/mac.fpv")
    os.popen("touch ./tmp/mac.fpv ./tmp/mac.danger ./data/mac.safe")
    print("Begin to initialize the system(about 10s)")
    initialize()
    os.popen("cp ./tmp/mac ./data/mac.safe")
    print("Initialize Over. Begin to Detect")
    while(1):
        scan()
        filter()
        if dangerMac:
            print("Danger Mac: ")
            os.system("cat ./tmp/mac.danger")
        detect()
        blinkLED()


statusMonitor = os.popen(r"iwconfig", "r").read()
os.system("clear")
print("Welcome to the UAVWarning system!\n")

if not re.search("Monitor", statusMonitor):
    print("Start the Monitor Mode on wlan1")
    excuteCommand("airmon-ng check kill")
    excuteCommand("airmon-ng start wlan1")
    print("Success!")
else:
    print("Already in Monitor Mode!\n")

while(1):
    order = input("请输入功能:")
    if order == "scan":
        print("Begin to Scan(about 4s)...")
        scan()
        filter()
        if dangerMac:
            print("Danger Mac:")
            os.system("cat ./tmp/mac.danger")
    elif order == "detect":
        detect()
    elif order == "initialize":
        print("Begin to Initialize(about 10s)...")
        initialize() 
        os.popen("cp ./tmp/mac ./data/mac.safe")
        print("Initialize Over!")
    elif order== "blink":
        blinkLED()
        print("Blink over")
    elif order== "help":
        os.system("cat README")
    elif order== "stay":
        stayLED()
        print("Stay Over")
    elif order== "exit":
        print("Bye~\n")
        exit(0)
    elif order=="auto":
        autoProcess()

    else:
        print("Unknown command: " + order)
    print()
            
