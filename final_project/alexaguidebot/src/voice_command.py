#!/usr/bin/env python2.7
import rospy
import roslib
import numpy as np
import json
import paho.mqtt.client as mqtt
from alexaguidebot.srv import Command
from alexaguidebot.srv import CommandRequest
from alexaguidebot.srv import CommandResponse

roslib.load_manifest('alexaguidebot');

COMMANDS_TOPIC="irobotucsd/commands/"
MQTT_BROKER_URL="broker.hivemq.com"
MQTT_BROKER_PORT=1883

def handle_message(msg):
    if msg.topic == COMMANDS_TOPIC:
        command_json = json.loads(msg.payload)
        command = command_json['command'];
        if command == "navigation":
            location = command_json['location'];
        rospy.wait_for_service("voice_commands")
        try:
            command_srv = rospy.ServiceProxy("voice_commands",Command)
            command_srv(CommandRequest.NAVIGATE,location)
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(COMMANDS_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    handle_message(msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

