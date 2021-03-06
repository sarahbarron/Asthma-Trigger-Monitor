#!/bin/bash
# Author: Sarah Barron
# Module: Computer Systems and Networks
# Assignment-2: IoT

# Description: Menu
# This script presents the user with a command line menu.
# This menu allows the user to input their desired asthma trigger settings

# Pattern for only numbers
NumberPattern="^[0-9]*$"

# This is a Function to check if a user has entered exit in the
# command prompt at any stage if they do this function will
# start the menu again
CheckForExit(){
	ExitPattern="^[eE][xX][iI][tT]$"
	if [[ $1 =~ $ExitPattern ]]
	then
        	clear
        	./startmenu.sh
		exit 0
	fi
}

clear
echo "=================================================================================================================================================="
echo "                             ASTHMA TRIGGER MONITOR SETUP                                                  "
echo "=================================================================================================================================================="
# Array of string options for the menu
options=('START SENSOR' 'View Current Settings' 'Set Ideal Sensor Settings' 'Set Ideal Temperature' 'Set Ideal Humidity' 'Set Ideal Indoor Air Quality' 'Set Remote Access' 'Reset to Default Settings' 'Quit')

# Prompt to user looking for a valid menu number
PS3=$'\n-------------------------------------------------------------------------------------------------------------------------------------------------\nEnter A Menu Number between 1 and 9 (press enter to view the menu again) : '

# prints each menu command on one column instead of rows using a column width of 27
# Ref: unix.stackexchange.com/questions/293604/bash-how-to-make-each-menu-selections-in-1-line-instead-of-multiple-selections
COLUMNS=27

# Select the name in the options array
# ref: linuxhint.com/bash_select_command/ 
# helped with printing string menu options using an array
select name in "${options[@]}"
do
case $name in

"START SENSOR")
	clear
        python sensor/indoor-air-quality.py
        ;;

# View the current min and max sensor settings
"View Current Settings")
        clear
	currentMinTemp=$(grep "minTemp" AsthmaTriggerSettings/settings.json| awk '{print $2}')
	currentMaxTemp=$(grep "maxTemp"  AsthmaTriggerSettings/settings.json| awk '{print $2}')
	currentMinHum=$(grep "minHum"  AsthmaTriggerSettings/settings.json| awk '{print $2}')
	currentMaxHum=$(grep "maxHum"  AsthmaTriggerSettings/settings.json| awk '{print $2}')
	currentMinIaq=$(grep "minIaq"  AsthmaTriggerSettings/settings.json| awk '{print $2}')
	currentMaxIaq=$(grep "maxIaq"  AsthmaTriggerSettings/settings.json| awk '{print $2}')
	currentRemoteAccess=$(grep "remote"  AsthmaTriggerSettings/settings.json| awk '{print $2}' | sed 's/"/ /g')

	echo
	echo "CURRENT SETTINGS ARE:"
	echo
	echo "TEMPERATURE: $currentMinTemp C - $currentMaxTemp C"
	echo
	echo "HUMIDITY: $currentMinHum% - $currentMaxHum%"
	echo
	echo "INDOOR AIR QUALITY: $currentMinIaq - $currentMaxIaq"
	echo
	echo "REMOTE ACCESS: $currentRemoteAccess"
	echo
	echo "You will be notified if the sensor readings go outside of the above ranges"
	;;

# Set all the users ideal sensor settings
"Set Ideal Sensor Settings")
	clear
	./AsthmaTriggerSettings/allSettings.sh
	;;

# Set the user ideal temperature settings
"Set Ideal Temperature")
	clear
	./AsthmaTriggerSettings/singleSettings.sh temp
	;;

# Set the users ideal Humidity settings
"Set Ideal Humidity")
	clear
	./AsthmaTriggerSettings/singleSettings.sh hum
        ;;

# Set the ideal Indoor Air Quality settings
"Set Ideal Indoor Air Quality")
	clear
 	./AsthmaTriggerSettings/singleSettings.sh iaq
        ;;

# Set if the user has remote access to devices such as humidifiers or temperature
"Set Remote Access")
	clear
	echo REMOTE ACCESS SETTINGS
	./AsthmaTriggerSettings/remoteAccess.sh
	;;

# Reset the min and max settings to the default settings
"Reset to Default Settings")
	clear
        echo "{
        \"minHum\": 30 ,
        \"maxHum\": 50 ,
        \"minTemp\": 18 ,
        \"maxTemp\": 21 ,
        \"minIaq\": 0 ,
        \"maxIaq\": 100 ,
        \"remoteAccess\": \"n\"
}" > AsthmaTriggerSettings/settings.json

        echo "Settings have been reset to Ideal Temperature (18-21 Degrees Celsius), Humidity (30-50%RH), Indoor Air Quality (0-100 IAQ), Remote Access: No"
        ;;

# Quit the program will be exited
"Quit")
  	break
  	;;

# If the user enters an invalid menu number the Main Menu is run again 
*)
	echo "INVALID OPTION, IT MUST BE A MENU OPTION BETWEEN 1 and 9"
  	;;
esac
done
# When a user chooses to quit the program message is show and the program is stopped
echo "You have chosen to quit the Asthma Trigger Menu"
echo "Have a nice day!"
exit 0
