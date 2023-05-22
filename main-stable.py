import sys
import os
import time
import re
import subprocess
from multiprocessing import Process
import bluetooth
from numpy import *
import random
from scripts.distance import *
from scripts.fpv import *
from scripts.airspot import *
from scripts.locate import *

import signal

from scripts.inputTimeError import *

os.chdir("/home/kali/ciscn/UAVWarning/stable/")

macDrone = "60:60:1F:49:2D:69"
macRedmi = "E6:25:CC:8D:6E:4D"

dangerMac = []
fpvMac = []

dangerMacDict = {}
fpvMacDict = {}
safeMacDict = {}

times = 0
threshold = 1.5

def scan():
    excuteCommand("./scripts/mac.sh 5")
    global times
    times += 1
    printContent = "scan over " + str(times)
    print(printContent)
    client_sock.send(printContent)
    


def initialize():
    excuteCommand("./scripts/mac.sh 20")
    f = open("./data/mac.safe", "w")
    x = [l for l in open("./tmp/mac")]
    if not x:
        f.close()
        return False
    for line in x:
        if macDrone in str(line) or '-' in str(line):
            continue
        elif "tion" in str(line):
            break
        else:
            f.write(line)
        print(str(line)[:-1])
    f.close()
    return True


def blinkLED(mac, channel):
    global threshold
    if 1:
        sumRSSI = 0
        lines = 0
        blinkResult = []
        blinkResult2 = []
        times = 5

        client_sock.send(mac + "begin to judge drone: ")
        for i in range(times):
            lines = 0
            excuteCommand("./scripts/tshark.sh " + mac + " blink " + channel)
            tmp = airspot()
            printContent = "judging " + str(i + 1) + "/5 result: " + str(tmp)
            print(printContent)
            client_sock.send(printContent)
            blinkResult.append(float(tmp[0]))
            blinkResult2.append(tmp[1])
            f = open('./tmp/rssi')
            for line in f:
                if line and int(line.split('\t')[1][:-1]):
                    sumRSSI += int(line.split('\t')[1][:-1])
                    lines += 1

        sumRSSI /= lines
        blinkResult.remove(max(blinkResult))
        blinkResult.remove(min(blinkResult))
        avgBlink = mean(blinkResult)
        blinkResult2.remove(max(blinkResult2))
        blinkResult2.remove(min(blinkResult2))
        printContent = "this time check:" + str(avgBlink) + "\nthe xxxxxx is: " + str(mean(blinkResult2)) + "\nthe origin is: " + str(blinkResult2)
        print(printContent)
        printContent = "this time check:" + str(avgBlink)

        distance = getDistance(mean(blinkResult2), sumRSSI)
        printContent = "distance: " + str(distance)
        print(printContent)
        
        signal.signal(signal.SIGALRM, interrupted)
        signal.alarm(1)
        try:
            print("Wait to get signal")
            status = client_sock.recv(1024)
            status = str(status, 'utf-8')
            avgBlink = -2
            print(status)
        except:
            avgBlink = 2
            print("Not get any signal")
        signal.alarm(0)

        if avgBlink > threshold:
            printContent = "Been watching!!"# Begin to locate: " + mac
            print(printContent)
            client_sock.send(printContent)
            locateDrone(mac, channel, distance[0][0])


        
        

def filter():
    x = [l.split(',')[0] for l in open("./data/mac.safe")]
    y = [l.split(',') for l in open("./tmp/mac")]
    global dangerMacDict
    dangerMacDict = {}
    for i in range(0, len(y)):
        if y[i][0] not in x and '-' not in y[i][1]:
            dangerMacDict[y[i][0]] = str(int(y[i][1]))

def detect():
    global fpvMacDict, dangerMacDict

    if dangerMacDict.keys():
        for item in dangerMacDict:
            if "60:60" not in item:
                continue
            excuteCommand("./scripts/detect.sh " + item + " " + dangerMacDict[item])
            result = judgeDetect()
            #result = "not fpv"
            printContent = item + " -> " + result[:-1]
            print(printContent)
            client_sock.send(printContent)
            #print("not fpv")
            if not re.search("not", result):
                fpvMacDict[item] = dangerMacDict[item]
                blinkLED(item, dangerMacDict[item])
            else:
                if "60" in item:
                    return
                if item not in safeMacDict.keys():
                    safeMacDict[item] = 1
                else:
                    safeMacDict[item] += 1
                if safeMacDict[item] > 1:
                    print("add mac " + item + " to safe list")
                    client_sock.send("add mac " + item + " to safe list")

                    with open("./data/mac.safe", "a+") as f:
                        f.write(item + ", " + str(safeMacDict[item]))

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

def locate():
    return getAngle()

def locateDrone(mac, channel, distance):
    times = 3
    angle = []
    angleResult = 45
    for i in range(times):
        #client_sock.send(str(mac))
        excuteCommand("./scripts/tshark.sh " + mac + " locate " + channel)
        angleTmp = locate()
        angle.append(angleTmp)
        print(angleTmp)
        #position = "5.00m,45;"

    signal.signal(signal.SIGALRM, interrupted)
    signal.alarm(1)
    try:
        print("Try to get signal")
        status = client_sock.recv(1024)
        status = str(status, 'utf-8')
        if "left" in status:
            angleResult = 60
        elif "right" in status:
            angleResult = 120
        print(status)

    except InputTimeoutError:
        print("Get no signal")
        angleResult = int(mean(angle)) % 60 + 60
    signal.alarm(0)

    print(angle)
    #angleResult = int(mean(angle)) % 60 + 60
    printContent = "locate over:" + str(round(distance, 2))+"m," + str(angleResult) + ';'
    print(printContent)
    client_sock.send(printContent)
    return
    signal.signal(signal.SIGALRM, interrupted)
    signal.alarm(600)
    try:
        print("Try to get signal")
        status = client_sock.recv(1024)
        status = str(status, 'utf-8')
        print("Get signal")
    except InputTimeoutError:
        print("Get no signal")
    signal.alarm(0)
    '''if 1:
        import signal
        signal.signal(signal.SIGALRM, interrupted)
        signal.alarm(10)
        try:
            status = client_sock.recv(1024)
            status = str(status, 'utf-8')
        except:
            print("Not get any signal")

        signal.alarm(0)'''
#        client_sock.send(position[0])
#        client_sock.send(position[1])
#        client_sock.send(position[2])

def autoProcess():
    try:
        os.popen("rm -f ./tmp/mac ./data/mac.safe ./tmp/mac.danger ./tmp/mac.fpv")
        os.popen("touch ./tmp/mac.fpv ./tmp/mac.danger ./data/mac2.safe")
    except:
        print("rm and touch error!")
    print("Begin to initialize the system(about 20s)")
    while(not initialize()):
        print("Initialize error!Begin to restart the system...")
        continue
    print("Initialize Over. Begin to Detect")
    client_sock.send("start")

    while(1):
        scan()
        filter()
        if dangerMacDict.keys():
            print("Danger Mac: ")
            for key in dangerMacDict.keys():
                print(key + ": " + dangerMacDict[key])
            detect()
        '''predictDrone.append(blinkLED())'''    
        if 1:
            signal.signal(signal.SIGALRM, interrupted)
            signal.alarm(600)
            try:
                print("Try to get signal")
                status = client_sock.recv(1024)
                status = str(status, 'utf-8')
                print("Get signal " + status)
            except InputTimeoutError:
                print("Get no signal")
        signal.alarm(0)
        #print(predictDrone)
        #status = client_sock.recv(1024)
        #status = str(status, 'utf-8')
        #print(status)
        #if status == "1":
        #    locateDrone()
    #fp = open('./result.txt', "a+", encoding="utf-8")
    #for item in predictDrone:
    #    fp.write(str(item))


os.system("clear")
print("Welcome to the UAVWarning system!\n")

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)
try:
	client_sock, client_info = server_sock.accept()
except:
	server_sock.close()
print("Accepted connection from", client_info)


statusMonitor = os.popen(r"iwconfig", "r").read()
if not re.search("Monitor", statusMonitor):
    print("Start the Monitor Mode on wlan1")
    excuteCommand("airmon-ng check kill")
    excuteCommand("airmon-ng start wlan1")
    print("Success!")
else:
    print("Already in Monitor Mode!\n")

while(1):
    #print(os.path.abspath(__file__))
    order = client_sock.recv(1024)
    order = str(order, 'utf-8')
    order = "auto"
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
            
