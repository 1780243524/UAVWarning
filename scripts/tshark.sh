#!/bin/bash
#get the wlan data

mac=$1
#mac=60:60:1f:49:2d:69
channel=$3
#channel=13
iwconfig wlan1 freq $channel
if [ $2 = "blink" ]; then
    python3 ./scripts/led-detect-6hz.py & tshark -i wlan1 -f "ether src $mac" -w ./tmp/tcapture.pcap -a duration:6 & wait
    #process=$(cat ./tmp/process)
    #kill $process
elif [ $2 = "locate" ]; then
    python3 ./scripts/led-spot-5-6hz.py & tshark -i wlan1 -f "ether src $mac" -w ./tmp/tcapture.pcap -a duration:6 & wait
    #process=$(cat ./tmp/process)
    #kill $process

else
    tshark -i wlan1 -f "ether src $mac" -w ./tmp/tcapture.pcap -a duration:6 & wait
fi

python3 ./scripts/turn-off.py
bash ./scripts/bitrate30.sh ./tmp/tcapture.pcap & wait
#tshark -i wlan0mon -Y "wlan.fc.type==2 and wlan.sa==60:60:1f:49:2d:69" -w tcapture.pcap -b duration:10 -w tmp
#tshark -i wlan0mon -w tcapture -f "ether src f4:2a:7d:ab:9f:38"
#tshark -i wlan0mon -w tcapture
# bash ./bitrate30.sh tcapture
