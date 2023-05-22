import sys
import os
import time
import re
import subprocess
from multiprocessing import Process
import bluetooth
import random
os.chdir("/home/kali/ciscn/UAVWarning/stable/")
macDrone = "60:60:1F:49:2D:69"
droneWatchFlag = 1
#channel = "13"
macRedmi = "E6:25:CC:8D:6E:4D"
#channel = "11"
dangerMac = []
fpvMac = []
dangerMacDict = {}
def scan():
    excuteCommand("./scripts/mac.sh 3")
    print("scan over")

#def detect(mac=mac, channel=channel):
#    return excuteCommand("./scripts/detect.sh " + mac + " " + channel)

def initialize():
    excuteCommand("./scripts/mac.sh 10")
    f = open("./data/mac.safe", "w")
    x = [l for l in open("./tmp/mac")]
    if not x:
        f.close()
        return False
    for line in x:
        print(str(line))
        if macDrone in str(line) or "tion" in str(line):
            #print(str(line))
            continue
        else:
            f.write(line)
    f.close()
    return True
    #os.popen("rm ./data/mac2.safe")
    #os.popen("mv ./data/mac2.safe ./data/mac.safe")


def blinkLED():
    resultDrone = {}
    
    for line in open("./tmp/mac.fpv"):
        sumBlink = 0
        for i in range(3):
            client_sock.send("blink")
            channel = line.split(" ")[1]
            mac = line.split(" ")[0]
            channel = 6
            mac = macRedmi
            print("Judging " + mac)
            excuteCommand("./scripts/tshark.sh " + mac + " bblink " + channel)
            #print("one time")
            with open('./tmp/res.txt', 'r') as f:
                predict = f.read()
                print(predict)
                sumBlink += float(predict)
                #list1 = list1.split(' ')
                #for i in range(0, len(list1)):
                #    list1[i] = list1[i].rstrip('\n')
                #predict = "predict:" + list1[0]
                #y_predict = "y_predict:" + list1[1]
                #print(predict)
                #print(y_predict)
                #client_sock.send(predict)
        sumBlink /= 3
        print("this time check:" + str(sumBlink) + "\n\n")
        #client_sock.send(sumBlink)
    return resultDrone

def stayLED():
    for line in open("./tmp/mac.fpv"):
        channel = line.split(" ")[1]
        mac = line.split(" ")[0]
        print("Judging " + mac)
        excuteCommand("./scripts/tshark.sh " + mac + " stay " + channel) 
        printBlank()

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
    pass
    #print("\r\b\r\b\r\b\r\b\r\b\r\b")
    #for i in range(6):
    #    print("                                                                                             ")
    #print("\r\b\r\b\r\b\r\b\r\b\r\b\r\b")

def locate(flag = 0):
    realAngle = 30
    ret = []
    angle = 0
    distence = 3
    if(flag == 0):
        angle = 90
    elif(flag == 1):
        seed = random.randint(0,10)
        if(seed < 8):
            angle = random.randint(90 - realAngle/2 - 5 , 90 - realAngle/2 + 5)
        else:
            angle = random.randint(90 - realAngle, 90)
    else:
        seed = random.randint(0,10)
        if(seed < 8):
            angle = random.randint(90 + realAngle/2 - 5, 90 - realAngle/2 + 5)
        else:
            angle = random.randint(90, 90 + realAngle)
    distence = distence + random.uniform(-0.5, 0.5)
    return [distence, angle, 0]

def locateDrone():
    #if droneWatchFlag == 0:
    #    return -1;
    for line in open("./tmp/drone.danger"):
        channel = line.split(" ")[1]
        mac = line.split(" ")[0]
    #    if predictDrone[mac] == -1:
    #        continue;
        client_sock.send(str(macDrone))
        print("locating " + mac)
        excuteCommand("./scripts/tshark.sh " + mac + " locate " + channel)
        printBlank()
        position = locate()
#        client_sock.send(position[0])
#        client_sock.send(position[1])
#        client_sock.send(position[2])

def autoProcess():
    '''try:
        os.popen("rm -f ./tmp/mac ./data/mac.safe ./tmp/mac.danger ./tmp/mac.fpv")
        os.popen("touch ./tmp/mac.fpv ./tmp/mac.danger ./data/mac2.safe")
    except:
        print("rm and touch error!")
    print("Begin to initialize the system(about 10s)")
    while(not initialize()):
        continue
    os.popen("cp ./tmp/mac ./data/mac2.safe")
    print("Initialize Over. Begin to Detect")
    client_sock.send("start")'''
    while(1):
        '''scan()
        #filter()
        if dangerMac:
            print("Danger Mac: ")
            os.system("cat ./tmp/mac.danger")
        detect()'''
        predictDrone = blinkLED() 
        #status = client_sock.recv(1024)
        #status = str(status, 'utf-8')
        #print(status)
        #if status == "1":
        #    locateDrone()


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
            
