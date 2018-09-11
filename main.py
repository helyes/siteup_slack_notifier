from __future__ import print_function

import os
import json
import requests
import urllib2
from datetime import datetime, timedelta

# Set webhook_url and CHANNEL to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
WEBHOOK_URL=os.environ['WEBHOOK_URL']
CHANNEL=os.environ['CHANNEL']
def validate(res, expected):
    '''Returns if res does not include expected
    '''
    return expected in res

def post_to_slack (text, icon_emoji, enabled):
    '''
    Posts message to slack
    if quiet parameter is True, only logging the message that would be posted
    '''
    slack_data = {         
            "channel": CHANNEL,
            "username": "Site poll",
            "text": text,
            "icon_emoji": icon_emoji
        }
    if not enabled:
        print ("Slack data: " + json.dumps(slack_data))
        return

    response = requests.post(
        WEBHOOK_URL, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def is_notification_enabled (event, result):
    '''
    Returns true if the notification should be sent 
    based on the given event and site check result
    '''
    is_success = result['result_code'] == 0
    return (is_success and event['report_success']) or ( not is_success and event['report_failure'])

def enrich_event (event):
    '''
    Adds default fields to event
    '''
    event.setdefault("report_failure", True)
    event.setdefault("report_success", False)
    event.setdefault("icon_emoji_failure", ":bomb:")
    event.setdefault("icon_emoji_success", ":champagne:")
    return event


def lambda_handler(event, context):
    now = datetime.now()
    enrich_event(event)
    ret = {
        "trigger_event": event,
        "start_at" : format(str(now)),
        "http_response_code" : 0
    }
    
    try:
        # need to validate trigger event
        print('Checking {} at {}...'.format(event['site'], format(str(now))))
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'AWS Lambda')]
        result = opener.open(event['site'])
        ret['http_response_code']= result.getcode()
        if not validate(result.read(), event['site_expected_text']):
            raise Exception('Validation failed.')

    except urllib2.HTTPError, ue:
        print('Check failed. ' + str(ue))
        ret['result_code'] = 1
        ret['result'] = event['site'] + " might be offline. " + str(ue)
        ret['http_response_code']= ue.code
    except urllib2.URLError, u:
        print('Check failed. ' + str(u))
        ret['result_code'] = 2
        ret['result'] = event['site'] + " might be offline. " + str(u)
    except Exception, e:
        print('Check failed. ' + str(e))
        ret['result_code'] = 3
        ret['result'] = event['site'] + " might be offline, did not found [" + event['site_expected_text'] + "]. " + str(e)
    else:
        print('Check passed. GET {} includes [{}]'.format(event['site'], event['site_expected_text']))
        ret['result_code'] = 0                
        ret['result'] = event['site'] + " is online. Found [" + event['site_expected_text'] + "]"        
    finally:
        opener.close()

    end_at = datetime.now()
    ret['end_at'] = format(str(end_at))
    ret['duration_ms'] = int((end_at - now).total_seconds() * 1000)
    #print('Check complete at {}'.format(str(datetime.now())))
    #print ("Response payload: " + json.dumps(ret ,indent=4, sort_keys=True))
    print ("Response payload: " + json.dumps(ret))
    ret['message']=ret['result'] + ". Response time: " + str(ret['duration_ms']) + "ms"
    if is_notification_enabled(event, ret):
        post_to_slack(ret['message'], 
                        event["icon_emoji_success"] if ret['result_code'] == 0  else event["icon_emoji_failure"], 
                        event['slack_enabled']
                        )     
    return ret

sample_event = {
    "site": 'https://app-stg.shiftcare.com',
    #"site": 'https://shift.free.beeceptor.com/my/api/path/1',    
    "site_expected_text": 'Sign in to start your session',
    "report_failure": True,
    "report_success": True,
    "slack_enabled": False,
   "icon_emoji_failure": ":sob:",
}

response=lambda_handler(sample_event,'B')
print ("\n---------------------\nResponse:\n" + json.dumps(response, indent=4, sort_keys=True))
#print ("Response:\n" + lambda_handler(sample_event,'B'))
