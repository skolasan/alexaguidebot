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

COMMANDS_TOPIC="irobotucsd/commands/"

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

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


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

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("chaitanya/topic1/#")
    client.publish("chaitanya/topic2/","move:right")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name=="SummonIntent":
        if 'MapPoint' in intent['slots']:
            data="{'command': 'summon', 'location':"+ intent['slots']['MapPoint']['value']+ "}"
            publish_mqtt_message(COMMANDS_TOPIC,data);
        session_attributes = {}
        speech_output = "I summoned the irobot to " + \
                    intent['slots']['MapPoint']['value'] +\
                    " ,It should be here any minute. Watch Out!"

        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
                                speech_output,should_end_session))
    
        
    elif intent_name=="NavigateIntent":
        if 'MapPoint' in intent['slots']:
            data="{'command': 'navigation', 'location':"+ intent['slots']['MapPoint']['value']+ "}"
            publish_mqtt_message(COMMANDS_TOPIC,data);
        session_attributes = {}
        speech_output = "I asked the irobot to navigate to" + \
                    intent['slots']['MapPoint']['value'] +\
                    " ,Please follow the robot!"
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
                                speech_output,should_end_session))
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


#Test code
test = {
  "session": {
    "sessionId": "SessionId.243764da-3982-4a33-831f-1466c157fadd",
    "application": {
      "applicationId": "amzn1.ask.skill.aaf60aa9-0cfb-48eb-a771-862a327ebf41"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AE24EMRJKG6YLPCJI5M4734NIEYLYR74ZOJ2TGNNSRON67XFLVQC5MTLIAJNPBABOLW65LGIMCUXAASE4HE4AIGC55AESYFLHW6UT2JLFA74Y2CPE7R5CNDYTDX7CHXXFJJSN76KT6GR3NVPKKFVZ5UEHETWQF4BAEIQHTFM423MIWPEEZG3LMEOODVVU2STRW4LRSEDJVPODVY"
    },
    "new": "true"
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.ecfd4f4a-cc58-4fd3-8632-b8d58d2efc65",
    "locale": "en-US",
    "timestamp": "2016-11-16T09:01:56Z",
    "intent": {
      "name": "SummonIntent",
      "slots": {
        "MapPoint": {
          "name": "MapPoint",
          "value": "zoneone"
        }
      }
    }
  },
  "version": "1.0"
}

test2 = {
  "session": {
    "sessionId": "SessionId.d28235fc-0c03-440f-b704-6b97324c79c0",
    "application": {
      "applicationId": "amzn1.ask.skill.aaf60aa9-0cfb-48eb-a771-862a327ebf41"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AE24EMRJKG6YLPCJI5M4734NIEYLYR74ZOJ2TGNNSRON67XFLVQC5MTLIAJNPBABOLW65LGIMCUXAASE4HE4AIGC55AESYFLHW6UT2JLFA74Y2CPE7R5CNDYTDX7CHXXFJJSN76KT6GR3NVPKKFVZ5UEHETWQF4BAEIQHTFM423MIWPEEZG3LMEOODVVU2STRW4LRSEDJVPODVY"
    },
    "new": "true"
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.c832ef87-eb8d-4487-9f12-ce53df55c211",
    "locale": "en-US",
    "timestamp": "2016-11-16T10:12:49Z",
    "intent": {
      "name": "NavigateIntent",
      "slots": {
        "MapPoint": {
          "name": "MapPoint",
          "value": "zone 1"
        }
      }
    }
  },
  "version": "1.0"
}
lambda_handler(test2,"jaffa")
