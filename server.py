from flask_app import app
from flask_app.controllers import quotes 
from apscheduler.schedulers.background import BackgroundScheduler
from flask_app.models.quote import Quote
from flask_app.models.user import User

#fills Quotes db from api if quotes db is empty
Quote.fill_DB()

# Checks DB for users requested text time, retrieves users who requested text for this hour (UTC time), retrieves unique quote, and initiates the text
#NEED TO DO: Change out the print statement for the Text API
#REQ: install APScheduler with pipenv install APScheduler
def text_quote():
    recipients = User.text_recipients()
    for recipient in recipients:
        quote = Quote.get_quote(recipient['id'])
        quote = quote['text']
        name = recipient['full_name']
        print(f"{name}'s quote of the day: {quote}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=text_quote, trigger="interval", seconds=60)
scheduler.start()


if __name__ == '__main__':
    app.run(debug=False)