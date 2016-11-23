"""
Test module for the lambda_function
"""

from lambda_function import *

def getCallerJson(intent_name,map_value):
    if(map_value == ""):
        return {
          "session": {
            "sessionId": "SessionId.a2ad871b-452e-484c-8793-cbe96fe5895b",
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
            "requestId": "EdwRequestId.27e566a7-348a-4f9e-a2ec-096cbe325e46",
            "locale": "en-US",
            "timestamp": "2016-11-23T06:52:52Z",
            "intent": {
              "name": intent_name,
              "slots": {
              }
            }
          },
          "version": "1.0"
        }

    else:
        return {
          "session": {
            "sessionId": "SessionId.a2ad871b-452e-484c-8793-cbe96fe5895b",
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
            "requestId": "EdwRequestId.27e566a7-348a-4f9e-a2ec-096cbe325e46",
            "locale": "en-US",
            "timestamp": "2016-11-23T06:52:52Z",
            "intent": {
              "name": intent_name,
              "slots": {
                "MapPoint": {
                  "name": "MapPoint",
                  "value": map_value
                }
              }
            }
          },
          "version": "1.0"
        }
    
context=""
#print lambda_handler(getCallerJson("QueryIntent","xyz"),context)
#print lambda_handler(getCallerJson("QueryIntent",""),context)
#print lambda_handler(getCallerJson("QueryIntent","water fountain"),context)
#print lambda_handler(getCallerJson("NavigateIntent","zone 1"),context)
#print lambda_handler(getCallerJson("NavigateIntent","zumber"),context)
#print lambda_handler(getCallerJson("NavigateIntent",""),context)
print lambda_handler(getCallerJson("AMAZON.HelpIntent","xyz"),context)
