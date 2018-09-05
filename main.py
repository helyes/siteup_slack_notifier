from __future__ import print_function

import os
import urllib2
from datetime import datetime, timedelta
import httplib, urllib

#DB_HOST = os.environ['DB_HOST']
#DB_PASSWORD = os.environ['DB_PASSWORD']

def validate(res, expected):
    '''Returns if res does not include expected
    '''
    return expected in res

def lambda_handler(event, context):
    now = datetime.now()
    ret = {
        "event": event,
        "start_at" : format(str(now))   
    }
    print('Checking {} at {}...'.format(event['site'], format(str(now))))
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'AWS Lambda')]
        if not validate(opener.open(event['site']).read(), event['site_expected_text']):
            raise Exception('Validation failed')
    except:
        print('Check failed! - posting message to slack')
        ret['result_code'] = 1
        ret['result'] = 'Check failed'     
        raise
    else:
        print('Check passed!')
        ret['result_code'] = 0                
        ret['result'] = 'Check passed!'        
    finally:
        end_at = datetime.now()
        ret['end_at'] = format(str(end_at))
        ret['duration_ms'] = int((end_at - now).total_seconds() * 1000)
        print('Check complete at {}'.format(str(datetime.now())))
        return ret

sample_event = {
    "site": 'https://app-stg.shiftcare.com',
    "site_expected_text": 'ShiftCare',
}

print (lambda_handler(sample_event,'B'))