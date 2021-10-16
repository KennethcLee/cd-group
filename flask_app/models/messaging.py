from twilio.rest import Client 

class Messaging:
    @classmethod
    def send_sms(cls, data):
        with open ("./flask_app/static/files/twilio.key", "r") as key:
            twilio_key=(key.read()).strip()
        with open ("./flask_app/static/files/twilio.account", "r") as account_id:
            twilio_account_id=(account_id.read()).strip()
        with open ("./flask_app/static/files/twilio.sid", "r") as messaging_sid:
            twilio_sid=(messaging_sid.read()).strip()
        # account_sid = twilio_account_id
        account_sid = twilio_sid
        auth_token = twilio_key
        client = Client(account_sid, auth_token)

        # print('***  1000A  ***', twilio_account_id, twilio_key, data['phone'])
        # Original Code Below
        # message = client.messages.create(
        #     messaging_service_sid=twilio_sid,
        #     body=data['message'],
        #     to=data['phone']
        #     )
        print('***  1000A  ***', twilio_sid, twilio_key, data['phone'])
        message = client.messages.create(
            to=data['phone'],
            from_="+13206264345",
            body=data['message']
        )
        print('message created')
        print(message)

        return(message.sid)