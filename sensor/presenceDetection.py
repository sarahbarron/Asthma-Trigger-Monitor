#!/usr/bin/env python
#coding=utf-8

import subprocess
import logging 
import os
# Do an arp-scan on the network and check if a mac address from the devices.dat file 
# is included in the arp scan. If it is the person is home if its not the person is
# not at home
def arp_scan():
	try:
		# MAC addresses of devices
		macs=[]

		# read in the contents of the device.dat file which contains names and mac addresses
		# of known devices in the house.
		file=open("sensor/home-devices.dat","r")

		# loop through each line of the file
		# For each line split the line and store it as an array
		# The first word in the split array is the name
		# The second word in the split array is the mac address
		# add the name to the names array and the mac to the macs array
		for line in file:
        		splitArray=line.split()
        		mac=splitArray[1]
        		macs.append(mac)

#		bluetoothScan = subprocess.check_output('sudo hcitool scan', shell=True)
#		for i in range(len(macs)):
#                   if macs[i] in bluetoothScan:
#                         print 'Home'
#                         return True

                arpScan = subprocess.check_output('sudo arp-scan -l', shell=True)
		for i in range(len(macs)):
			if macs[i] in arpScan:
				print 'Home'
				return True


		print "Nobody is Home don't send notifications"
		return False


	except Exception as e:
		logging.error(e)
