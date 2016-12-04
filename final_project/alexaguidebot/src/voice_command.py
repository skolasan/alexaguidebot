#!/usr/bin/env python2.7
import rospy
import roslib
import numpy as np
import json
import paho.mqtt.client as mqtt
from alexaguidebot.srv import Command
from alexaguidebot.srv import CommandRequest
from alexaguidebot.srv import CommandResponse

from pprint import pprint

roslib.load_manifest('alexaguidebot');

COMMANDS_TOPIC="irobotucsd/commands/"
RESPONSE_TOPIC_BASE="irobotucsd/responses/"

MQTT_BROKER_URL="broker.hivemq.com"
MQTT_BROKER_PORT=1883

def handle_message(client,msg):
    if msg.topic == COMMANDS_TOPIC:
        command_json = json.JSONDecoder().decode(str(msg.payload))
        pprint(command_json)
        command = command_json["command"];
        if command == "navigation":
            location = command_json["location"];
            rospy.wait_for_service("voice_commands")
            try:
                command_srv = rospy.ServiceProxy("voice_commands",Command)
                command_srv(CommandRequest.NAVIGATE,location)
            except rospy.ServiceException, e:
                print "Service call failed: %s" % e

        if command == "locate":
            reqid = command_json['reqid']
            rospy.wait_for_service("voice_commands")
            payload=""
            try:
                print("locate called")
                command_srv = rospy.ServiceProxy("voice_commands",Command)
                locate_resp = command_srv(CommandRequest.LOCATE,"")
                payload = locate_resp.message
                client.publish(RESPONSE_TOPIC_BASE+str(reqid),payload)
            except rospy.ServiceException, e:
                payload="error"
                print "Service call failed: %s" % e

            client.publish(RESPONSE_TOPIC_BASE+str(reqid),payload)
                            
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(COMMANDS_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    handle_message(client,msg)

rospy.init_node('voice_commands', anonymous=True)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)

try:
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
except KeyboardInterrupt:
    # Be a good citizen
    client.disconnect()
