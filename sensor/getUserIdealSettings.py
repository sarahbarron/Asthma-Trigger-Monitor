#!/usr/bin/env python

# Author: Sarah Barron
# Module: Computer Systems and Networks
# Assignment-2: IoT

import json

# read in the contents of the settings.json file
# assign values to the min and max sensor values and 
# return the values to the main program

def getAllSettings():
    with open('AsthmaTriggerSettings/settings.json') as json_file:
        settings = json.load(json_file)

    minTemp = settings['minTemp']
    maxTemp = settings['maxTemp']
    minHum = settings['minHum']
    maxHum = settings['maxHum']
    minIaq = settings['minIaq']
    maxIaq = settings['maxIaq']
    remoteAccess = settings['remoteAccess']
    return(minTemp, maxTemp, minHum, maxHum, minIaq, maxIaq, remoteAccess)
