import nexmo
client = nexmo.Client(key='45c66121',secret='mS6lAGqRwOhnoSNS')

response = client.send_message({'from': '84979578136', 'to': '+84979578136', 'text': 'Hello world'})

response = response['messages'][0]

if response['status'] == '0':
  print ('Sent message', response['message-id'])

  print ('Remaining balance is', response['remaining-balance'])
else:
  print ('Error:', response['error-text'])
