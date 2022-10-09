# PublishToWebhookSlack
#!/usr/bin/python3.9

import urllib3
import json

http = urllib3.PoolManager()

def lambda_handler(event, context):
    
    url = "https://hooks.slack.com/services/<TOKEN>"
    msg = event['Records'][0]['Sns']['Message']
    msg_dict = json.loads(msg)
    aws_account_id = context.invoked_function_arn.split(":")[4]
    
    msg2 = {
        "channel": "#channel_name",
        "username": "CloudWatch",
        "text": msg_dict['AlarmName']+"\n"+msg_dict['NewStateReason']+"\n"+msg_dict['AlarmDescription']+"\n"+'AccountID: '+aws_account_id+"\n",
        "icon_emoji": ":"
    }
    
    encoded_msg = json.dumps(msg2).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
    
    print({
        "message": event['Records'][0]['Sns']['Message'],
        "status_code": resp.status,
        "response": resp.data
    })
    