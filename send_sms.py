from twilio.rest import Client
accountSid = "ACcd3d96cc5d3fcfa8832eb4a5571e0367"
authToken = "85c0fb37fc0391d718a65af9a604d6ab"
twilioClient = Client(accountSid, authToken)
myTwilioNumber = "+18563228547"
destCellPhone = "+84979578136"
myMessage = twilioClient.messages.create(body = "whatever", from_=myTwilioNumber, to=destCellPhone)