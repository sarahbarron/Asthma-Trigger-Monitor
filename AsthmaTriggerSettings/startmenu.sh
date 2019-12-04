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
options=('Initial Setup' 'Reset to Default Settings' 'Set Ideal Temperature' 'Set Ideal Humidity' 'Set Ideal Indoor Air Quality' 'Set Remote Access' 'Quit')

# Prompt to user looking for a valid menu number
PS3=$'\n-------------------------------------------------------------------------------------------------------------------------------------------------\nEnter A Menu Number between 1 and 7 (press enter to view the menu again) : '

# prints each menu command on one column instead of rows using a column width of 27
# Ref: unix.stackexchange.com/questions/293604/bash-how-to-make-each-menu-selections-in-1-line-instead-of-multiple-selections
COLUMNS=27

# Select the name in the options array
# ref: linuxhint.com/bash_select_command/ 
# helped with printing string menu options using an array
select name in "${options[@]}"
do
case $name in

"Initial Setup")
	clear
	./allSettings.sh
	;;

"Reset to Default Settings")
	echo "{
	\"minHum\": 30
	\"maxHum\": 50
	\"minTemp\": 18
	\"maxTemp\": 21
	\"minIaq\": 0
	\"maxIaq\": 100
	\"remoteAccess\": n
	\"settingsChanged\": y
}" > settings.json

	echo "Settings have been reset to Ideal Temperature (18-21 Degrees Celsius), Humidity (30-50%RH), Indoor Air Quality (0-100 IAQ), Remote Access: No"
	;;
"Set Ideal Temperature")
	clear
	./singleSettings.sh temp
	;;

"Set Ideal Humidity")
	clear
	./singleSettings.sh hum
        ;;


"Set Ideal Indoor Air Quality")
	clear
 	./singleSettings.sh iaq
        ;;

"Set Remote Access")
	echo REMOTE ACCESS SETTINGS
	./remoteAccess.sh
	;;


# If the user selects 6 to quit the program will be exited
"Quit")
  	break
  	;;

# If the user enters an invalid menu number the Main Menu is run again 
*)
	echo "INVALID OPTION, IT MUST BE A MENU OPTION BETWEEN 1 and 6"
  	;;
esac
done
# When a user chooses to quit the program message is show and the program is stopped
echo "You have chosen to quit the Asthma Trigger Menu"
echo "Have a nice day!"
exit 0
