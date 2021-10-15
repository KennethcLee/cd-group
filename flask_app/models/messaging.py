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
        account_sid = twilio_account_id
        auth_token = twilio_key
        client = Client(account_sid, auth_token)

        print('***  1000A  ***', twilio_account_id, twilio_key, data['phone'])
        message = client.messages.create(
            messaging_service_sid=twilio_sid,
            body=data['message'],
            to=data['phone']
            )

        return(message.sid)