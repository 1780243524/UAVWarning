#!/bin/bash
# get the interval time
prefix=12
suffix=1
interval=0.033333333333
name=$(date)
name="./tmp/aggregation"
echo $name
# get the capture data
tshark -q -z 'io,stat,'"$interval" -r "$1" -Y "wlan.fc.type==2"> "$1".txt -2
# get the rssi data
#tshark -r "$1" -Tfields -e frame.time_relative -e radiotap.dbm_antsignal -Y "wlan.fc.type==2" > ./tmp/rssi
tshark -r "$1" -Tfields -e frame.time_relative -e radiotap.dbm_antsignal > ./tmp/rssi
# get the lines
lines=$(wc -l < "$1".txt)
line_2_remove="$((lines - prefix))"
#echo $line_2_remove
#echo $lines
tail --lines=$line_2_remove "$1".txt > ./tmp/tmp.txt
lines=$(wc -l < ./tmp/tmp.txt)
line_2_remove="$((lines - sefix))"
head --lines=$line_2_remove ./tmp/tmp.txt > ./tmp/tmp2.txt
cut -f 3 -d '|' ./tmp/tmp2.txt > ./tmp/tmp3.txt
cut -f 4 -d '|' ./tmp/tmp2.txt > ./tmp/tmp4.txt
cat ./tmp/tmp3.txt > ./tmp/packets.txt | tr -d "\t\n\ r"
cat ./tmp/tmp4.txt > ./tmp/bytes.txt | tr -d "\t\n\ r"
echo ’packets’| cat - ./tmp/packets.txt > ./tmp/temp && mv ./tmp/temp ./tmp/packets.txt
echo ’bytes ’ | cat - ./tmp/bytes.txt > ./tmp/temp && mv ./tmp/temp ./tmp/bytes.txt
#paste -d "," packets.txt bytes.txt >> "$1".csv
paste -d "," ./tmp/packets.txt ./tmp/bytes.txt >> "$1".csv
rm ./tmp/packets.txt ./tmp/bytes.txt "$1".txt ./tmp/tmp4.txt ./tmp/tmp3.txt ./tmp/tmp2.txt ./tmp/tmp.txt
paste -d "," ./tmp/*csv >> ./tmp/all.txt
rm ./tmp/*.csv
echo $name
tr -d "\t" < ./tmp/all.txt > "$name".txt
rm ./tmp/all.txt
sed -i '1d' "$name".txt
sed -i '$d' "$name".txt
#python3 drawrssi.py
#lines=$(wc -l < ./tmp/aggregation.txt)
#python3 ./scripts/airspot.py $lines
