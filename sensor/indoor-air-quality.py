#!/usr/bin/env python

import bme680
import time
import urllib2
import time
import blynklib
import os
from getUserIdealSettings import getAllSettings
from wia import Wia
from presenceDetection import arp_scan


###################### USER SETTINGSS #############################################################################################
arp_scan()
# Get user settings for when to send notifications
(minTemp, maxTemp, minHum, maxHum, minIaq, maxIaq, remoteAccess) = getAllSettings()
userRemoteAccess = str(remoteAccess)

# if the user has remote access to home devices don't do any arp scans (set to false)
# Otherwise do an arp scan to see if someone is home
if userRemoteAccess == 'y':
    doArpScan = False
    notify = True
else:
    doArpScan = True

# Previous Values set to ideal min and max values on first setup and also
# if a user doesn't have remote access and are not at home when they return home
# the previous values are reset to the ideal min and max values need for comparison


previousTemp = minTemp
previousHum = minHum
previousIaq = minIaq

######################### INITIALISE IoT's ###########################################################################################

# Initialise Thingspeak
WRITE_API_KEY = os.environ.get('THINGSPEAK_WRITE_API')
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY

# Initialise Blynk
BLYNK_AUTH = os.environ.get('BLYNK_AUTH')
blynk = blynklib.Blynk(BLYNK_AUTH)


# Inistialise Wia
wia = Wia()
wia.access_token = os.environ.get('WIA_TOKEN')


#############################   IoT FUNCTIONS ##########################################################################################

# Takes in the current temperature, humidity and iaq values
# sends the values to Blynk, Wia and ThingSpeak
def WriteDataToCloudIoTs(temp, hum, iaq):

    # send the data to thingspeak in the query string
    conn = urllib2.urlopen(
        baseURL + '&field1=%s&field2=%s&field3=%s' % (temp, hum, iaq))
    print(conn.read())
    # Closing the connection
    conn.close()

    # send values to WIA
    wia.Event.publish(name="temperature", data=temp)
    wia.Event.publish(name="humidity", data=hum)
    wia.Event.publish(name="IAQ", data=iaq)

    # set the temperature pin colors for Blynk
    if temp < 18 or temp > 21:
        # if temp is between 16 and 23 set to orange
        if temp >= 16 and temp <= 23:
            blynk.set_property(1, 'color', '#FF7E00')
        # if temp is less than 16 or greater than 23 set color to red
        else:
            blynk.set_property(1, 'color', '#FF0400')
    # if temp is in range 18-21 set color to green
    else:
        blynk.set_property(1, 'color', '#00E400')

    # set the humidity pin colors
    if hum > 50 or hum < 30:
        # if humidity is out of ideal range and is less than 55 or greater than 25
        # set the color to orange
        if hum <= 55 and hum >= 25:
            blynk.set_property(2, 'color', '#FF7E00')
        # if humidity is greater than 55 or less than 25 set to red
        else:
            blynk.set_property(2, 'color', '#FF0400')
    # otherwise if it is in range set it to green
    else:
        blynk.set_property(2, 'color', '#00E400')

    # Set the IAQ pin colors for each range in line with
    # the standard colors for IAQ levels
    # 0-50 Green
    if iaq >= 0 and iaq <= 50:
        blynk.set_property(3, 'color', '#00E400')
    # 51-100 Yellow
    if iaq >= 51 and iaq <= 100:
        blynk.set_property(3, 'color', '#FFFF00')
    # 101-150 Orange
    if iaq >= 101 and iaq <= 150:
        blynk.set_property(3, 'color', '#FF7E00')
    # 151-200 Red
    if iaq >= 151 and iaq <= 200:
        blynk.set_property(3, 'color', '#FF0400')
    # 201-300 Purple
    if iaq >= 201 and iaq <= 300:
        blynk.set_property(3, 'color', '#8F3F97')
    # 301+ Burgundy
    if iaq >= 301:
        blynk.set_property(3, 'color', '#7E0123')

    # write values to Blynk
    blynk.virtual_write(1, temp)
    blynk.virtual_write(2, hum)
    blynk.virtual_write(3, iaq)

# if the user doesn't have remote access to devices
# when the user is not home keep the previousTemp as the
# users ideal values so that when the user returns home the
# values are compared against ideal values and if they are
# out of range the first notification can be initialised


def setPreviousValues():
    previousTemp = minTemp
    previousHum = minHum
    previousIaq = minIaq

# Function to check if a notification to blynk is needed


def isNotificationNeeded(temp, hum, iaq):
        # set send notification to false initially
    tempSendNotification = False
    humSendNotification = False
    iaqSendNotification = False

    # If the previous measurement was in range and the
    # current measurement is out of range then send a notification
    # this means that a notification will only be sent once
    # when it moves from in range to out of range and not
    # everytime it stays out of range
    if(previousTemp >= minTemp and previousTemp <= maxTemp):
        if(temp < minTemp or temp > maxTemp):
            tempSendNotification = True
    if(previousHum >= minHum and previousHum <= maxHum):
        if(hum < minHum or hum > maxHum):
            humSendNotification = True
    if(previousIaq >= minIaq or previousIaq <= maxIaq):
        if(iaq < minIaq or iaq > maxIaq):
            iaqSendNotification = True

    # if any of the values go from in range to out of range send a blynk notification
    if(tempSendNotification or humSendNotification or iaqSendNotification):
        # if the temperature needs to be notified set the notifyTemp to
        # the temp value otherwise set it to a trigger value of -100
        if tempSendNotification:
            notifyTemp = temp
        else:
            notifyTemp = -100

        # if the humidity needs to be notified set the notifyHum to
        # the hum value otherwise set it to a trigger value of -1
        if humSendNotification:
            notifyHum = hum
        else:
            notifyHum = -1

        # if the IAQ needs to be notified set the notifyIaq to
        # the iaq value otherwise set it to a trigger value of -1
        if iaqSendNotification:
            notifyIaq = iaq
        else:
            notifyIaq = -1

        # send values to blynkNotification method
        blynkNotification(notifyTemp, notifyHum, notifyIaq)


# Function to send a Blynk Notification
def blynkNotification(temp, hum, iaq):

    # initialise the message to empty initially when a value
    # is detected as out of range the message will change
    tempMessage = ''
    humMessage = ''
    iaqMessage = ''

    # if the temperature is out of range set the
    # appropriate message
    if temp > -100 and temp < minTemp:
        tempMessage = 'Temperature is low: ' + \
            str(temp)+"C\n- Turn on the heating"
    elif temp > -100 and temp > maxTemp:
        tempMessage = 'Temperature is high: ' + \
            str(temp) + "C\n- Turn off the heating"

    # if the humidity is out of range set the
    # appropriate message
    if hum > -1 and hum < minHum:
        humMessage = 'Humidity is low: ' + \
            str(hum)+"%\n- Turn on the humidifier"
    elif hum > -1 and hum > maxHum:
        humMessage = 'Humidity is high: ' + \
            str(hum)+"%\n- Turn on the dehumidifier"

    # if the IAQ is out of range set the
    # appropriate message
    if iaq > -1 and iaq > maxIaq:
        print iaq
        IAQmeasurement = 'Index Air Quality (IAQ): '+str(iaq)+' : '
        IAQcauses = "\n- Some causes: gas, fire, dust, smoking, hairspray etc."

        if(iaq > 100 and iaq <= 150):
            levelOfConcern = "Unhealthy for Asthmas Sufferers"
        elif(iaq > 150 and iaq <= 200):
            levelOfConcern = "Unhealthy for everyone"
        elif(iaq > 200 and iaq <= 300):
            levelOfConcern = "Very Unhealthy for everyone"
        elif (iaq > 300):
            levelOfConcern = "Hazardous"
        else:
            levelOfConcern = "This is outside your desired IAQ levels"

        iaqMessage = IAQmeasurement+levelOfConcern+IAQcauses

    # append the messages
    message = tempMessage+'\n\n'+humMessage+'\n\n'+iaqMessage

    # send the blynk notification
    blynk.notify(message)


######################################### SENSOR - INITIAL SETUP ##############################################################################
# try link to the sensor
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Set the oversampling settings
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

# Set gas measurements
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# start_time and curr_time ensure that the
# burn_in_time (in seconds) is kept track of.
start_time = time.time()
curr_time = time.time()
burn_in_time = 5

# create an array to store burn in data
burn_in_data = []

try:
    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.
    print('Collecting gas resistance burn-in data for 5 mins\n')
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            print('Gas: {0} Ohms'.format(gas))
            time.sleep(1)

    # gas baseline is the sum of the last 50 values in the array
    # divided by 50 to get the average value
    gas_baseline = sum(burn_in_data[-50:]) / 50.0

    # Set the humidity baseline to 40%, an optimal indoor humidity.
    hum_baseline = 40.0

    # Sets the balance between humidity and gas reading in the
    # calculation of air_quality_score (25:75, humidity:gas)
    # humidity contributes to 25% of the IAQ measurement
    hum_weighting = 0.25

    print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(
        gas_baseline,
        hum_baseline))

    # get the temperature reading. which is returned in celsius
    temp = round(sensor.data.temperature, 1)

################################# INFINITE LOOP #############################################################################

    # Continue to loop
    while True:

        blynk.run()
        # if the sensor is receiving data and the heat_stable is true
        if sensor.get_sensor_data() and sensor.data.heat_stable:

            # get the gas reading (ohms)
            gas = sensor.data.gas_resistance
            gas_offset = gas_baseline - gas

            # get the humidity reading
            hum = sensor.data.humidity
            hum_offset = hum - hum_baseline

            # Calculate hum_score as the distance from the hum_baseline (40).
            # If the humidity is higher than the optimum value of 40
            # calculate the precentage that humidity contributes to the 25% of the IAQ
            if hum_offset > 0:
                hum_score = (100 - hum_baseline - hum_offset)
                hum_score /= (100 - hum_baseline)
                hum_score *= (hum_weighting * 100)

            # otherwise if the humidity value is below the optimum value of 40
            # calculate the precentage that humidity contributes to the 25% of the IAQ
            else:
                hum_score = (hum_baseline + hum_offset)
                hum_score /= hum_baseline
                hum_score *= (hum_weighting * 100)

            # Calculate gas_score as the distance from the gas_baseline.
            if gas_offset > 0:
                gas_score = (gas / gas_baseline)
                gas_score *= (100 - (hum_weighting * 100))

            else:
                gas_score = 100 - (hum_weighting * 100)

            # Calculate air_quality_score.
            index_air_quality = (100 - (hum_score + gas_score)) * 5

            # get the temperature reading
            temp = round(sensor.data.temperature, 1)
            hum = round(hum, 1)
            iaq = round(index_air_quality, 1)

            # sends the data to the cloud IoTs Blynk and Thingspeak
            WriteDataToCloudIoTs(temp, hum, iaq)

            # if the user has no remote access to devices do a presence detection
            # to check if they are home
            if doArpScan:
                notify = arp_scan()

            # if the user is home or they have remote access to devices check if they need a notification
            if notify:
                print previousHum
                print previousTemp
                print previousIaq
                isNotificationNeeded(temp, hum, iaq)

                # update the previous measurement for the next loop
                previousTemp = temp
                previousHum = hum
                previousIaq = iaq
            else:
                # reset the values so when the user returns home,
                # a check will be done to see if the current values are out of the users ideal range
                setPreviousValues()

            # print message to terminal
            print('temp: {0:.2f} Celsius, humidity: {1:.2f} %RH, air quality: {2:.2f}'.format(
                temp,
                hum,
                iaq))
            # sleep for 1 Minute
            time.sleep(15)

# if there is a keyboard interrupt do nothing
except KeyboardInterrupt:
    pass
