#!/bin/bash
#get the wlan data
mac=$1
channel=$2
#channel=13
#mac=60:60:1f:49:2d:69
iwconfig wlan1 freq $channel
tshark -i wlan1 -f "ether src $mac" -w ./tmp/tcapture.pcap -a duration:5
#tshark -i wlan1 -f "ether src 60:60:1f:49:2d:69" -w tcapture.pcap -a duration:5
result=$(bash ./scripts/bitrate80.sh ./tmp/tcapture.pcap)
echo $result
#if [ ${#result} -ne 13 ];then
#	echo $result
#	echo "Drone:"$mac
#	echo "Danger! begin to detect...."
#	bash tshark.sh $mac
	#bash bitrate30.sh tcapture.pcap
#else
#	echo $result
#	echo ""
#fi
# tshark -i wlan0mon -f "ether src 60:60:1f:49:2d:69" -w tcapture.pcap
#tshark -i wlan0mon -Y "wlan.fc.type==2 and wlan.sa==60:60:1f:49:2d:69" -w tcapture.pcap -b duration:10 -w tmp
#tshark -i wlan0mon -w tcapture -f "ether src f4:2a:7d:ab:9f:38"
#tshark -i wlan0mon -w tcapture
# bash ./bitrate30.sh tcapture
