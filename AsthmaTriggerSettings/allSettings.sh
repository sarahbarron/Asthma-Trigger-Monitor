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

# read in the settings from the settings.json file
currentMinTemp=$(grep "minTemp" AsthmaTriggerSettings/settings.json| awk '{print $2}')
currentMaxTemp=$(grep "maxTemp" AsthmaTriggerSettings/settings.json| awk '{print $2}')
currentMinHum=$(grep "minHum" AsthmaTriggerSettings/settings.json| awk '{print $2}')
currentMaxHum=$(grep "maxHum" AsthmaTriggerSettings/settings.json| awk '{print $2}')
currentMinIaq=$(grep "minIaq" AsthmaTriggerSettings/settings.json| awk '{print $2}')
currentMaxIaq=$(grep "maxIaq" AsthmaTriggerSettings/settings.json| awk '{print $2}')
currentRemoteAccess=$(grep "remote" AsthmaTriggerSettings/settings.json| awk '{print $2}')
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
if [ "$currentMinIaq" == "0" ]
then
	echo "You will be notified if the the indoor air quality goes above $currentMaxIaq IAQ"
else
	echo "You will be notified if the the indoor air quality goes below $currentMinIaq IAQ or above $currentMaxIaq IAQ"
fi
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

# If the user does not want to keep the current settings. Go through each sensor type and
# ask they user if they want to change the notification range on that sensor type
# Run the singleSettings.sh file for each of the sensor ranges the user wants to change
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
        	./AsthmaTriggerSettings/singleSettings.sh temp all
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
        	./AsthmaTriggerSettings/singleSettings.sh hum all
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
        	./AsthmaTriggerSettings/singleSettings.sh iaq all
	fi
        echo
	echo "-------------------------------------------------------------------------------------------------------------------------------------------------"
	./AsthmaTriggerSettings/remoteAccess.sh

fi
echo
echo "THANK YOU FOR TAKING THE TIME TO SETUP YOUR ASTHMA TRIGGER MONITOR. ALL SETTINGS HAVE BEEN RECORDED"
echo
exit 0
