#!/usr/bin/env python

import bme680
import time
import urllib2
import time
import BlynkLib
import blynklib
import os
from wia import Wia

# set the previous temperatures to in range values
previousTemp = 21
previousHum = 40
previousIAQ = 50


# Initialise Thingspeak
WRITE_API_KEY = os.environ.get('THINGSPEAK_WRITE_API')
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY

# Initialise Blynk
BLYNK_AUTH = os.environ.get('BLYNK_AUTH')
blynk = blynklib.Blynk(BLYNK_AUTH)


# Inistialise Wia
wia = Wia()
wia.access_token = "d_sk_vIE1YYvy2J4diOY04CzxPZwK"


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

    # set the temperature pin colors
    if temp < 19 or temp > 23:
        # if temp is between 18 and 24 set to orange
        if temp >= 18 and temp <= 24:
            blynk.set_property(1, 'color', '#FF7E00')
        # if temp is less than 18 or greater than 24 set color to red
        else:
            blynk.set_property(1, 'color', '#FF0400')
    # if temp is in range 19-23 set color to green
    else:
        blynk.set_property(1, 'color', '#00E400')

    # set the humidity pin colors
    if hum > 50 or hum < 30:
        # if humidity is out of ideal range and is less than 60 or greater than 20
        # set the color to orange
        if hum <= 60 and hum >= 20:
            blynk.set_property(2, 'color', '#FF7E00')
        # if humidity is greater than 60 or less than 20 set to red
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


# Function to send a Blynk Notification
def blynkNotification(temp, hum, iaq):
    # initialise the message to empty initially when a value
    # is detected as out of range the message will change
    tempMessage = ''
    humMessage = ''
    iaqMessage = ''

    # if the temperature is out of range set the
    # appropriate message
    if temp > -100 and temp < 19:
        tempMessage = 'Temperature is low: ' + \
            str(temp)+"C\n- Turn on the heating"
    elif temp > -100 and temp > 23:
        tempMessage = 'Temperature is high: ' + \
            str(temp) + "C\n- Turn off the heating"

    # if the humidity is out of range set the
    # appropriate message
    if hum > -1 and hum < 30:
        humMessage = 'Humidity is low: ' + \
            str(hum)+"%\n- Turn on the humidifier"
    elif hum > -1 and hum > 50:
        humMessage = 'Humidity is high: ' + \
            str(hum)+"%\n- Turn on the dehumidifier"

    # if the IAQ is out of range set the
    # appropriate message
    if iaq > -1 and iaq > 100:
        IAQmeasurement = 'Index Air Quality (IAQ): '+str(iaq)+' : '
        IAQcauses = "\n- Some causes: gas, fire, dust, smoking, humidity etc."
        if(iaq > 100 and iaq <= 150):
            levelOfConcern = "Unhealthy for Asthmas Sufferers"
        elif(iaq > 150 and iaq <= 200):
            levelOfConcern = "Unhealthy for everyone"
        elif(iaq > 200 and iaq <= 300):
            levelOfConcern = "Very Unhealthy for everyone"
        else:
            levelOfConcern = "Hazardous"
        iaqMessage = IAQmeasurement+levelOfConcern+IAQcauses
    # append the messages
    message = tempMessage+'\n\n'+humMessage+'\n\n'+iaqMessage
    # send the blynk notification
    blynk.notify(message)


######################################### Initial Setup ##############################################################################
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
burn_in_time = 300

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
            # otherwise if the humidity value is equal to below the optimum value of 40
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
            index_air_quality = hum_score + gas_score

            # get the temperature reading
            temp = round(sensor.data.temperature, 1)
            hum = round(hum, 1)
            iaq = round(index_air_quality, 1)

            # sends the data to the cloud IoTs Blynk and Thingspeak
            WriteDataToCloudIoTs(temp, hum, iaq)

            # Testing values
            # WriteDataToCloudIoTs(20, 50, 260)

            # set send notification to false initially
            tempSendNotification = False
            humSendNotification = False
            iaqSendNotification = False
            # If the previous measurement was in range and the
            # current measurement is out of range then send a notification
            # this means that a notification will only be sent once and not
            # everytime it stays out of range
            if(previousTemp > 19 and previousTemp < 23):
                if(temp < 19 or temp > 23):
                    tempSendNotification = True
            if(previousHum > 30 and previousHum < 50):
                if(hum < 30 or hum > 50):
                    humSendNotification = True
            if(previousIAQ <= 100):
                if(iaq > 100):
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
                blynkNotification(notifyTemp, notifyHum, notifyIaq)

                # Testing values
                # blynkNotification(20, 50, 260)

            # update the previous measurement for the next loop
            previousTemp = temp
            previousHum = hum
            previousIAQ = iaq

            # print message to terminal
            print('temp: {0:.2f} Celsius, humidity: {1:.2f} %RH, gas: {0:.2f} omhs, air quality: {2:.2f}'.format(
                temp,
                hum,
                gas,
                iaq))
            # sleep for 5 seconds
            time.sleep(60)

# if there is a keyboard interrupt do nothing
except KeyboardInterrupt:
    pass
