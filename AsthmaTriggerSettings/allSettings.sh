#!/bin/bash
# Author: Sarah Barron
# Module: Computer Systems and Networks
# Assignment-2: IoT 

# Description: Add User Settings for Asthma Trigger Monitor
# A script which updates the Asthma Trigger Settings File with details of the
# users temperature, humidity, indoor air quality, and remote access details.



# Function to check if a user has entered exit at any stage 
# which brings the user back to the main menu
CheckForExit(){
ExitPattern="^[eE][xX][iI][tT]$"
if [[ $1 =~ $ExitPattern ]]
then
        exit 0
fi

}
currentMinTemp=$(grep "minTemp" settings.json| awk '{print $2}')
currentMaxTemp=$(grep "maxTemp" settings.json| awk '{print $2}')
currentMinHum=$(grep "minHum" settings.json| awk '{print $2}')
currentMaxHum=$(grep "maxHum" settings.json| awk '{print $2}')
currentMinIaq=$(grep "minHum" settings.json| awk '{print $2}')
currentMaxIaq=$(grep "maxHum" settings.json| awk '{print $2}')
currentRemoteAccess=$(grep "remote" settings.json| awk '{print $2}')
YorN=""

echo
echo "THE CURRENT SETTINGS ARE:"
echo
echo "TEMPERATURE:"
echo "You will be notified if the the temperature goes below $currentMinTemp C or above $currentMaxTemp C"
echo
echo "HUMIDITY:"
echo "You will be notified if the the humidity goes below $currentMinHum %RH or above $currentMaxHum %RH"
echo
echo "INDOOR AIR QUALITY"
echo "You will be notified if the the indoor air quality goes below $currentMinIaq IAQ or above $currentMaxIaq IAQ"
echo
echo "REMOTE ACCESS"

if [ "$currentRemoteAccess" == "y" ]
then
	echo "YES - There is remote access to devices such as heating, humidifier or dehumidifier"
else
	echo "NO - There is no remote access to devices such as heating, humidifier or dehumidifier"
fi

echo "-------------------------------------------------------------------------------------------------------------------------------------------------"
until [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ] || [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
do
	echo
	printf "Are you happy to keep all of the above settings (y/n or exit to return to main menu) : "
	read YorN
	CheckForExit "$YorN"
done

if [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
then

	YorN=""
	until [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ] || [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
	do
		echo
		echo "-------------------------------------------------------------------------------------------------------------------------------------------------"
		echo
        	printf "Do you want to change the current temperature settings ($currentMinTemp C - $currentMaxTemp C) (y/n or exit to return to main menu) : "
        	read YorN
        	CheckForExit "$YorN"
	done

	if [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ]
	then
        	./singleSettings.sh temp all
	fi

	YorN=""
	until [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ] || [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
	do
		echo
		echo "-------------------------------------------------------------------------------------------------------------------------------------------------"
		echo
        	printf "Do you want to change the current Humidity settings ($currentMinHum %%RH - $currentMaxHum %%RH) (y/n or exit to return to main menu) : "
        	read YorN
        	CheckForExit "$YorN"
	done

	if [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ]
	then
        	./singleSettings.sh hum all
	fi

	YorN=""
	until [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ] || [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
	do
		echo
		echo "-------------------------------------------------------------------------------------------------------------------------------------------------"
		echo
        	printf "Do you want to change the current Indoor Air Quality settings ($currentMinIaq IAQ - $currentMaxIaq IAQ) (y/n or exit to return to main menu) : "
        	read YorN
        	CheckForExit "$YorN"
	done

	if [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ]
	then
        	./singleSettings.sh iaq all
	fi
        echo
	echo "-------------------------------------------------------------------------------------------------------------------------------------------------"
	./remoteAccess.sh

fi
echo
echo "THANK YOU FOR TAKING THE TIME TO SETUP YOUR ASTHMA TRIGGER MONITOR. ALL SETTINGS HAVE BEEN RECORDED"
echo
exit 0





