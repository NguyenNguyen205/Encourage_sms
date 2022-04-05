"""This is my first project"""
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
import requests
import json
import os
from decouple import config

# used api: lukePeavy/quotable
# get env : config(key)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)


# storing each user name, phone number, quotes they get
class User(db.Model):
    """User model to store user data"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<{self.name}>"


@app.route('/', methods=['GET', 'POST'])
def main_page():
    # Get prefix
    with open('phone_prefix.json') as prefix:
        country_prefix = json.load(prefix)

    return render_template('main.html', country_prefix=country_prefix)


@app.route('/reply', methods=['POST', 'GET'])
def reply_page():
    username = request.form['name']
    phone = "+" + str(request.form['prefix'] + request.form['phone'])
    response = requests.get('https://api.quotable.io/random')
    message = response.json()['content']
    new_user = User(name=username, phone_number=phone, message=message)
    db.session.add(new_user)
    db.session.commit()
    account_sid = config('USER')
    token = config('KEY')
    client = Client(account_sid, token)
    try:
        sms_message = client.messages.create(
            to=phone,
            from_='+18126356557',
            body=message
        )
    except:
        print('Something wrong')

    return render_template('reply.html')


if __name__ == '__main__':
    app.run(debug=True)


