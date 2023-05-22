#筛选危险MAC
(python3 mac.py )> mac.danger

# 对危险MAC进行操作
while read line
do
	mac=${line:2:17}
	channel=${line#*,}
	channel=${channel%?}
	echo ""
	echo $channel,$mac
	bash detect.sh $mac $channel
done < mac.danger
