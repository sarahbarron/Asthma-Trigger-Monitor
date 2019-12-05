##!/bin/bash
# Author: Sarah Barron
# Module: Computer Systems and Networks
# Assignment-2: IoT

# Initially the settings are set to the ideal settings for an asthmas sufferer
# Temperature = 18-21 degrees celcius
# Humidity = 30% - 50% RH
# Indoor Air Quality = 0 - 100 IAQ
# The user has the option to change these settings to values that suit their
# Asthma condition better but are not allowed to set values that would be 
# considered unhealty for Asthma Sufferes 
# eg: max humidity can only be 59%RH as above this level can encourage mold growth



# Indoor Air Quality Settings
if [  "$1" == "iaq" ]
then
	idealMin=0
	idealMax=100
	minLevel=0
	maxLevel=150
	sense="Indoor Air Quality"
	symbol="IAQ"
	pattern="^[0-9]$|^[1-9][0-9]$|^1[0-4][0-9]$|^150$"
	min="minIaq"
	max="maxIaq"

# Temperature settings
elif [ "$1" == "temp" ]
then
	idealMin=18
	idealMax=21
	minLevel=16
        maxLevel=23
        sense="Temperature"
        symbol="C"
	pattern="^1[6-9]$|^2[0-3]$"
	min="minTemp"
	max="maxTemp"

# Humidity Settings
elif [ "$1" == "hum" ]
then
	idealMin=30
	idealMax=50
        minLevel=25
        maxLevel=55
        sense="Humidity"
        symbol='RH'
	pattern="^2[5-9]$|^3[0-9]$|^4[0-9]$|^5[0-5]$"
	min="minHum"
	max="maxHum"
fi

# Initial variable for yes or no set to blank
YorN=""
lowerLevel=$(grep "$min" AsthmaTriggerSettings/settings.json| awk '{print $2}')
higherLevel=$(grep "$max" AsthmaTriggerSettings/settings.json| awk '{print $2}')

# This is a Function to check if a user has entered exit in the
# command prompt at any stage if they do this function will
# start the settings menu again
CheckForExit(){
	ExitPattern="^[eE][xX][iI][tT]$"
	if [[ $1 =~ $ExitPattern ]]
	then
		exit 0
	fi
}


echo
# Get user input for the settings
echo "Ideal $sense Settings"
echo "-------------------------------------------------------------------------------------------------------------------------------------------------------"
echo
echo "The Ideal $sense is between $idealMin $symbol - $idealMax $symbol for an Asthma Sufferer"


# Ask the user if they want to keep the current settings or not
until [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ] || [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
do
	# This if statement is used so as to not ask the user if they want to change settings twice during initail setup
	if [ "$2" != "all" ]
	then
 		echo
	        echo "The current settings mean you will get a smartphone notification if the $sense goes below $lowerLevel $symbol and above $higherLevel $symbol"
		echo
	       	printf "Are you happy to keep the current settings of $lowerLevel - $higherLevel $symbol (y/n or exit to return to the main menu) : "
		read YorN
	else
		YorN="n"
	fi
        CheckForExit "$YorN"
        echo
done

# If the user chooses not to keep the current settings ask the user to enter the lower & higher levels - Integers are only allowed
# and must match a regex pattern 
if [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
then
        echo "Enter the lowest level that the $sense can go (must be greater than $minLevel or less than $maxLevel)"
	printf "(or exit to return to main menu): "
        read newLowerLevel
        CheckForExit "$newLowerLevel"
        until [[ $newLowerLevel =~ $pattern ]]
        do
		echo
        	echo "The value must be above $minLevel and less than $maxLevel (numbers only)"
                printf "Enter your ideal lowest $sense value (exit to return to main menu): "
                read newLowerLevel
                CheckForExit "$newLowerLevel"
        done

	lowerLevel=$newLowerLevel

	# if the user enters the max level that can be set  as their ideal lowest humidity level 
	# then the higher humidty level is set to  the same value
	# ask the user to enter the higher humidity level they want
	if [[ $lowerLevel -ne $maxLevel ]]
	then
		echo
		echo "Enter the highest level that the $sense can go (must be between $lowerLevel and $maxLevel)"
		printf "(or enter exit to return to the main menu) : "
		read newHigherLevel
       		CheckForExit "$newHigherLevel"
        	until [[ $newHigherLevel =~ $pattern && $newHigherLevel -ge $lowerLevel ]]
        	do
                	echo
			echo "The $sense value must be between $lowerLevel and $maxLevel"
                	printf "Enter your ideal highest $sense level (exit to return to main menu): "
                	read newHigherLevel
                	CheckForExit "$newHigherLevel"
        	done
		higherLevel=$newHigherLevel
	fi
	higherLevel=$newHigherLevel

fi


sed -i "s/$min.*/$min\": $lowerLevel ,/" AsthmaTriggerSettings/settings.json
sed -i "s/$max.*/$max\": $higherLevel ,/" AsthmaTriggerSettings/settings.json

echo
echo "You will be notified when the $sense goes: below $lowerLevel $symbol and above $higherLevel $symbol"
echo
exit 0
