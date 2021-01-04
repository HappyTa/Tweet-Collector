from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import keywordRequestForm
import tweepy
import json

# setting up OAuth for tweepy
auth = tweepy.OAuthHandler('gO5fX87uAaal7b8ZPk1gc3Lmr', 'bDk9Iq3cv6y3HKJNokrmz996HrGRlAqgAtBDYoCItKnnv68m1c')
auth.set_access_token('812320410511544320-gD8kcpRhsVFoxkcDETd9Rfgj7zO5Ocs', 'Y1bMqq2w9HuK6QHHMD2nac4idgqbtPpOz3vqGG2MfFE9k')
api = tweepy.API(auth)

# initialize the flask program
app = Flask(__name__)
app.config['SECRET_KEY'] = '7c4387868ee2c40bf5aecb48d5e7be09c7c9a142f5ead60c8c267780a94cbdbb'

# initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Setting up the database and its columns
class Tweets(db.Model):
    tweetId = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"tweet('{self.tweetId}', '{self.content}')" 

# A route for the homepage
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = keywordRequestForm()
    if form.validate_on_submit():
        flash(f'keyword(s) recieved! Printing out Tweets', 'success')
        keyword = form.keyword.data
        processed_keyword = keyword.split(',')

        for x in processed_keyword:
            #collected_Tweets = api.search(q=x, lang='en')
            for tweet in tweepy.Cursor(api.search, q=x, lang='en').items(100):
                
                # Adding new tweet to the database
                newTweet = Tweets(tweetId=tweet.id,content = tweet.text)
                db.session.add(newTweet)
                db.session.commit()

                # convert Tweets to strings
                json_str = json.dumps(tweet._json)

                # deserialise strings into python objects
                parsed = json.loads(json_str)
                with open("Tweets.json", 'a+') as outfile:
                    json.dump(parsed,outfile, indent = 4)

        return redirect(url_for('tweetprint'))
    return render_template('home.html', title = "Home page", form=form)

# About page
@app.route("/tweetprint", methods=['GET','POST'])
def tweetprint():
    return render_template('tweetprint.html', title = "tweetprint page")


# Use when the flask is run from python
if __name__ == "__main__":
    app.run(debug=True)