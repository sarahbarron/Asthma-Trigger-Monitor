#!/bin/bash
# Author: Sarah Barron
# Module: Computer Systems and Networks
# Assignment-2: IoT

# Description: Remote Access
# Ask the user if they have remote access to devices such as heating, humidifier or dehumidifier.
# Record the users input in the settings.txt file

# This is a Function to check if a user has entered exit in the
# command prompt at any stage if they do this function will
# start the menu again
CheckForExit(){
        ExitPattern="^[eE][xX][iI][tT]$"
        if [[ $1 =~ $ExitPattern ]]
        then
                exit 0
        fi
}

YorN=""
until [ "$YorN" = 'y' ] || [ "$YorN" = 'Y' ] || [ "$YorN" = 'n' ] || [ "$YorN" = 'N' ]
do
	echo
        printf "Do you have access to set your temperature or humidity levels remotely (y/n or exit to return to the main menu) : "
        read YorN
        CheckForExit "$YorN"
        echo
done
sed -i "s/remote.*/remoteAccess\": \"$YorN\"/" AsthmaTriggerSettings/settings.json
