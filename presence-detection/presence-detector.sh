#! /bin/bash

# presence-detect.sh
# searches for the MAC address of home devices

# do arp_scan to get connected mac addresses
connectedDevices=$(sudo arp-scan -l)

# read in the list of household devices to detect if they are home or not
# For each mac address in the home-devices file check if it is on the 
# arp-scan list of mac addresses
# If any device from the home-devices list is detected on the arp-scan 
# this means there is someone home exit with a 0 status
# Otherwise there is no-one so exit with a 1 status 
while read -r line 
	do
		mac=`echo $line|awk '{print $2}'`
		present=`echo $connectedDevices | grep $mac | wc -l`
		if [ $present -ne 0 ]
		then
			echo "Someone is home"
			exit 0
		fi
	done < home-devices.dat

echo "Nobody home"
exit 1
