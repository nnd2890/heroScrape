import requests
import json
def notify():
    api_key = 'DKG8TZBUJTZF53AOHIFDFJL88'
    notification_title = 'Some title to send'
    notification_message = 'Some message to send'
    url = "https://www.notifymydevice.com/push"
    data = {"ApiKey": api_key, "PushTitle": notification_title,"PushText": notification_message}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print ('Notification sent!')
    else:
        print ('Error while sending notificaton!')