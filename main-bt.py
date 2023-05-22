import sys
import os
import time
import re
import subprocess
from multiprocessing import Process
import bluetooth
#str1 = os.popen(r"iwconfig", "r").read()
#i = os.system("clear")
#print(str1)
#print(str1)
#其实并没有用到
strStatus = ""
# mode number 其实也没有用到
SaveAggregation = 1 #保存aggregation文件
ShowConfig = 0
Scan = 1
Blink = 1
Stay = 0


mac = "60:60:1f:49:2d:69"
channel = "13"
#mac = "E6:25:CC:8D:6E:4D"
#channel = "11"
dangerMac = []
fpvMac = []
dangerMacDict = {}
def scan():
    excuteCommand("mac.sh 3")
    print("scan over")

def detect(mac=mac, channel=channel):
    return excuteCommand("detect.sh " + mac + " " + channel)

def initialize():
    excuteCommand("mac.sh 10 > tttmp")

def blinkLED():
    for line in open("mac.fpv"):
        data = "blink"
        client_sock.send(data)
        channel = line.split(" ")[1]
        mac = line.split(" ")[0]
        print("Judging " + mac)
        excuteCommand("tshark.sh " + mac + " blink " + channel)
        #printBlank()
        with open('res.txt', 'r') as f:
            list1 = f.readlines()
            for i in range(0, len(list1)):
                list1[i] = list1[i].rstrip('\n')
        predict = "predict:" + list1[0] + "\n"
        client_sock.send(predict)
        print(predict)
       # y_predict = "y_predict:" + list1[1]
       # client_sock.send(y_predict)
       # print(predict)
		
            

def stayLED():
    for line in open("mac.fpv"):
        channel = line.split(" ")[1]
        mac = line.split(" ")[0]
        print("Judging " + mac)
        excuteCommand("tshark.sh " + mac + " stay " + channel) 
        printBlank()


def clearScreen():
    os.system("clear")
    print(strStatus)

#过滤危险MAC地址
def filter():
    x = [l.split(',')[0] for l in open("mac.safe")]
    y = [l.split(',') for l in open("mac")]
    global dangerMac
    dangerMac = []
    for item in y:
        item[1] = int(item[1])
    for i in range(0, len(y)):
        if y[i][0] not in x:
            dangerMac += y[i]
    f = open("mac.danger", "w")
    if dangerMac:
        f = open("mac.danger", "w")
        for i in range(0, len(dangerMac), 2):
            f.write(dangerMac[i] + " " + str(dangerMac[i + 1] ) + '\n')
    f.close()

def blink(mac=mac, blink="blink"):
    command = os.popen("bash tshark.sh " + mac + " " + blink)
    time.sleep(15)
    return command

def detect():
    global strStatus, fpvMac
    dangerMac = [l.split(' ') for l in open("mac.danger")]
    if dangerMac:
        for item in dangerMac:
            result = excuteCommand("detect.sh " + item[0] + " " + item[1][:-1])
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
                    with open("mac.safe", "a+") as f:
                        f.write(item[0] + ", " + item[1])
        f = open("mac.fpv", "w")
        for i in range(0, len(fpvMac), 2):
            f.write(fpvMac[i] + " " + fpvMac[i+1])
            data = fpvMac[i] + " " + fpvMac[i+1]
            client_sock.send(data)
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
    os.popen("rm -f mac mac.safe,mac mac.danger mac.fpv")
    os.popen("touch mac.fpv mac.danger mac.safe")
    print("Begin to initialize the system(about 10s)")
    initialize()
    os.popen("cp mac mac.safe")
    print("Initialize Over. Begin to Detect")
    data = "start"
    client_sock.send("start")
    print("begin while")
    while(1):
        scan()
        filter()
        if dangerMac:
            print("Danger Mac: ")
            os.system("cat mac.danger")
        detect()
        blinkLED()


statusMonitor = os.popen(r"iwconfig", "r").read()
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

if not re.search("Monitor", statusMonitor):
    print("Start the Monitor Mode on wlan1")
    excuteCommand("airmon-ng check kill")
    excuteCommand("airmon-ng start wlan1")
    print("Success!")
else:
    print("Already in Monitor Mode!\n")

while(1):
    #order = input("请输入功能:")
    print(os.path.abspath(__file__))
    order = client_sock.recv(1024)
    #print("Received", order)
    order = str(order, 'utf=8')
    #print("Received", order)
    if order == "scan":
        print("Begin to Scan(about 4s)...")
        scan()
        filter()
        if dangerMac:
            print("Danger Mac:")
            os.system("cat mac.danger")
    elif order == "detect":
        detect()
    elif order == "initialize":
        print("Begin to Initialize(about 10s)...")
        initialize() 
        os.popen("cp mac mac.safe")
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
        client_sock.close()
        server_sock.close()
        exit(0)
    elif order=="auto":
        autoProcess()

    else:
        print("Unknown command: " + order)
    print()
            
