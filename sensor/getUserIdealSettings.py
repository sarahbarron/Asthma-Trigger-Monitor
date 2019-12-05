import json


def allSettings():
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
