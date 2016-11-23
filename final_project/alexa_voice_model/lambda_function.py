"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import paho.mqtt.client as mqtt
import time
import random
import json as json

locations=["zone 1","zone 2","zone 3","elevator","restroom","home","water fountain"]

COMMANDS_TOPIC="irobotucsd/commands/"
RESPONSE_TOPIC_BASE="irobotucsd/responses/"

MQTT_BROKER_URL="broker.hivemq.com"
MQTT_BROKER_PORT=1883

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def publish_mqtt_message(topic,message):
    client = mqtt.Client()
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start();
    (result,mid)=client.publish(topic,message);
    time.sleep(1)
    client.loop_stop();
    client.disconnect();

def publish_nav_command(target):
    data={}
    data["command"] = "navigation"
    data["location"] = target
    data_json = json.JSONEncoder().encode(data)
    publish_mqtt_message(COMMANDS_TOPIC,data_json);


def on_message(client,userdata,msg):
    global callbackRx
    global outputRx
    callbackRx=True
    outputRx = msg.payload
    print("Locate response received: "+outputRx)

def call_mqtt_service(command):
    #construct the command json
    command_json={}
    global callbackRx
    global outputRx
    callbackRx=False
    outputRx=""
    #reqid=random.randint(1, 100)
    reqid=57
    command_json['command']=command
    command_json['reqid']=reqid
    command_json=json.JSONEncoder().encode(command_json);
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER_URL,MQTT_BROKER_PORT,60)
    time.sleep(1)
    client.subscribe(RESPONSE_TOPIC_BASE+str(reqid))
    (result,mid)=client.publish(COMMANDS_TOPIC,command_json)
    
    loopcount=0
    while callbackRx==False and loopcount < 6:
        client.loop(1)
        loopcount=loopcount+1
    if(callbackRx):
        print("wohoo!")
        callbackRx=False
        client.disconnect()
        return (True,outputRx)
    else:
        client.disconnect()
        print("Timeout")
        return (False,outputRx)

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    speech_output = "Welcome to the Alexa Guide bot. " \
                    "I can command the Guide bot for you, " \
                    "Try Saying, Where is the bot? or " \
                    "Ask bot to come to the elevator"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what would you like to do,"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def handle_session_end_request():
    speech_output = "Thank you for trying the Alexa Guide Bot. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
            speech_output,should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "SummonIntent":
        if 'MapPoint' in intent['slots']:
            if intent['slots']['MapPoint']['value'] in locations:
                publish_nav_command(intent['slots']['MapPoint']['value'])
                session_attributes = {}
                speech_output = "I summoned the bot to " + \
                        intent['slots']['MapPoint']['value'] +\
                        " ,It should be here any minute. Watch Out!"
            else:
                speech_output = "The bot don't know how to get to "+ \
                        intent['slots']['MapPoint']['value'] + \
                        ",Please Try again with a familiar place. for example, elevator. or waterfountain."
        else:
            speech_output = "You asked me to summon the robot but I don't know your location!" + \
            ", Try saying call the bot to the elevator"

        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
                                    speech_output,should_end_session))

    elif intent_name=="NavigateIntent":
        if 'MapPoint' in intent['slots']:
            if intent['slots']['MapPoint']['value'] in locations:
                publish_nav_command(intent['slots']['MapPoint']['value'])
                session_attributes = {}
                speech_output = "I asked the bot to navigate to " + \
                        intent['slots']['MapPoint']['value'] +\
                        " , Please follow the robot!"
            else:
                speech_output = "The bot don't know how to get to "+ \
                        intent['slots']['MapPoint']['value'] + \
                        ", Please Try again with a familiar place. for example, elevator. or waterfountain."
        else:
            speech_output = "You asked me to send a navigation command but I don't know your destination!" + \
            ", Try saying, take me to the elevator"
        session_attributes = {}                
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
                                speech_output,should_end_session))

    elif intent_name=="LocateIntent":
        (result,output) = call_mqtt_service("locate")
        session_attributes = {}
        should_end_session = True

        if result == True:
            speech_output = "The bot is currently closest to "+output
        else:
            speech_output = "There is a problem contacting the bot, Try again" \
                                " after sometime"

        return build_response(session_attributes, build_speechlet_response(
                                speech_output,should_end_session))

    elif intent_name=="QueryIntent":
        if 'MapPoint' in intent['slots']:
            if intent['slots']['MapPoint']['value'] in locations:
                speech_output="Yes, the bot can happily got to "+intent['slots']['MapPoint']['value']
            else:
                speech_output="Sorry, the bot don't know how to reach "+intent['slots']['MapPoint']['value']+ \
                                ", If you think its important, contact Team Centurions"
        else:
            speech_output="No, Offcourse I can't go to undefined places"
        session_attributes = {}
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
                                speech_output,should_end_session))


    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()

    else:
        raise ValueError("Invalid intent")



def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

#call_mqtt_service("locate")

#Test code
#test = {
  #"session": {
    #"sessionId": "SessionId.243764da-3982-4a33-831f-1466c157fadd",
    #"application": {
      #"applicationId": "amzn1.ask.skill.aaf60aa9-0cfb-48eb-a771-862a327ebf41"
    #},
    #"attributes": {},
    #"user": {
      #"userId": "amzn1.ask.account.AE24EMRJKG6YLPCJI5M4734NIEYLYR74ZOJ2TGNNSRON67XFLVQC5MTLIAJNPBABOLW65LGIMCUXAASE4HE4AIGC55AESYFLHW6UT2JLFA74Y2CPE7R5CNDYTDX7CHXXFJJSN76KT6GR3NVPKKFVZ5UEHETWQF4BAEIQHTFM423MIWPEEZG3LMEOODVVU2STRW4LRSEDJVPODVY"
    #},
    #"new": "true"
  #},
  #"request": {
    #"type": "IntentRequest",
    #"requestId": "EdwRequestId.ecfd4f4a-cc58-4fd3-8632-b8d58d2efc65",
    #"locale": "en-US",
    #"timestamp": "2016-11-16T09:01:56Z",
    #"intent": {
      #"name": "SummonIntent",
      #"slots": {
        #"MapPoint": {
          #"name": "MapPoint",
          #"value": "zoneone"
        #}
      #}
    #}
  #},
  #"version": "1.0"
#}

#test2 = {
  #"session": {
    #"sessionId": "SessionId.d28235fc-0c03-440f-b704-6b97324c79c0",
    #"application": {
      #"applicationId": "amzn1.ask.skill.aaf60aa9-0cfb-48eb-a771-862a327ebf41"
    #},
    #"attributes": {},
    #"user": {
      #"userId": "amzn1.ask.account.AE24EMRJKG6YLPCJI5M4734NIEYLYR74ZOJ2TGNNSRON67XFLVQC5MTLIAJNPBABOLW65LGIMCUXAASE4HE4AIGC55AESYFLHW6UT2JLFA74Y2CPE7R5CNDYTDX7CHXXFJJSN76KT6GR3NVPKKFVZ5UEHETWQF4BAEIQHTFM423MIWPEEZG3LMEOODVVU2STRW4LRSEDJVPODVY"
    #},
    #"new": "true"
  #},
  #"request": {
    #"type": "IntentRequest",
    #"requestId": "EdwRequestId.c832ef87-eb8d-4487-9f12-ce53df55c211",
    #"locale": "en-US",
    #"timestamp": "2016-11-16T10:12:49Z",
    #"intent": {
      #"name": "NavigateIntent",
      #"slots": {
        #"MapPoint": {
          #"name": "MapPoint",
          #"value": "zone 1"
        #}
      #}
    #}
  #},
  #"version": "1.0"
#}
#lambda_handler(test2,"jaffa")
