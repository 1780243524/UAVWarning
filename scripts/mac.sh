#!/bin/bash
#搜索并保存mac
#airodump-ng -w mac wlan1
rm -f ./tmp/mac-0* 
bash ./scripts/scan.sh $1 & wait
#处理扫描结果
mv ./tmp/mac-01.csv ./tmp/result
sed -i '1d' ./tmp/result
sed -i '1d' ./tmp/result
#只保留MAC和信道
cut -d ',' -f 1,4 ./tmp/result > ./tmp/mac
rm ./tmp/result
rm ./tmp/mac-01.*
tmp=$(tail -n 1 ./tmp/mac)
i=${#tmp}
if [ ${#tmp} -eq 1 ];then
	sed -i '$d' ./tmp/mac
	tmp=$(tail -n 1 ./tmp/mac)
fi

while [ ${#tmp} -gt 1 ]
do
	#echo $i
	sed -i '$d' ./tmp/mac
	tmp=$(tail -n 1 ./tmp/mac)
	#i=${#tmp}
done
sed -i '$d' ./tmp/mac
echo ""
#筛选危险MAC
#python3 mac.py > mac.danger

# 对危险MAC进行操作
#while read line
#do
#	mac=${line:2:17}
#	channel=${line#*,}
#	channel=${channel%?}
#	echo ""
#	echo $channel,$mac
#	bash detect.sh $mac $channel
#done < mac.danger
