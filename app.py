from multiprocessing.connection import wait
from pickle import TRUE
from tracemalloc import stop
from xml.etree.ElementTree import tostring
import requests
import sys
import os
import json
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import time

APIKeyDEV = "oQ6yzKZQUiqFbEUk"
APIKeyPROD = "HB7skR885Pgz73gi"
monitorBaseURL = "http://www.wienerlinien.at/ogd_realtime/monitor"
malfunctionURL = "http://www.wienerlinien.at/ogd_realtime/trafficInfoList?name=stoerunglang&sender=" + APIKeyDEV

MQTT_HOST = "192.168.0.102"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC_BASE = "WrLinien"
MQTT_USER = "admin"
MQTT_PW = "v6TKTgNxPg9M"
PUBLISH_INTERVAL = 30 #in seconds


#Create MQTT Client
version = '3' # or '3' 
mytransport = 'tcp' # or 'tcp'

client = mqtt.Client(client_id="WrLinienToMQTTApp",
                         transport=mytransport,
                         protocol=mqtt.MQTTv311,
                         clean_session=True)
client.username_pw_set(MQTT_USER, MQTT_PW)


while(TRUE):
    stopinfo = requests.get(monitorBaseURL + "?" + "rbl=4629&rbl=4640&&sender=" + APIKeyDEV).json()
    trafficInfos = requests.get(malfunctionURL).json()
    
    #Publish Monitors
    for monitor in stopinfo['data']['monitors']:
        locationName = monitor['locationStop']['properties']['title']
        for line in monitor['lines']:
            lineName=stopinfo['data']['monitors'][0]['lines'][0]['name'] 
            towards = line["towards"]
            lineCountdown = line['departures']['departure'][00]['departureTime']['countdown']

            client.connect(MQTT_HOST,MQTT_PORT,MQTT_KEEPALIVE_INTERVAL)
            client.publish(MQTT_TOPIC_BASE + "/" +locationName+ "/" + lineName + "/" + towards  ,lineCountdown)
            client.disconnect()

    #Publish TrafficInfo
    for trafficInfo in trafficInfos['data']['trafficInfos']:
        title = trafficInfo["title"]
        description = trafficInfo["description"]

        for relatedLine in trafficInfo["relatedLines"]:

            client.connect(MQTT_HOST,MQTT_PORT,MQTT_KEEPALIVE_INTERVAL)
            client.publish(MQTT_TOPIC_BASE + "/TrafficInfo/" + relatedLine, title + " - " + description)
        
    time.sleep(PUBLISH_INTERVAL)







