from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import keywordRequestForm
import tweepy

auth = tweepy.OAuthHandler('gO5fX87uAaal7b8ZPk1gc3Lmr', 'bDk9Iq3cv6y3HKJNokrmz996HrGRlAqgAtBDYoCItKnnv68m1c')
auth.set_access_token('812320410511544320-gD8kcpRhsVFoxkcDETd9Rfgj7zO5Ocs', 'Y1bMqq2w9HuK6QHHMD2nac4idgqbtPpOz3vqGG2MfFE9k')
api = tweepy.API(auth)


app = Flask(__name__)
app.config['SECRET_KEY'] = '7c4387868ee2c40bf5aecb48d5e7be09c7c9a142f5ead60c8c267780a94cbdbb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class tweets(db.Model):
    tweetId = db.Column(db.Integer, primary_key=True)
    authorId = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.tweet}')" 

# A route for the homepage
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = keywordRequestForm()
    if form.validate_on_submit():
        flash(f'keyword(s) recieved! Printing out tweets', 'success') 
        return redirect(url_for('tweetprint'))
    return render_template('home.html', title = "Home page", form=form)

# About page
@app.route("/tweetprint", methods=['POST'])
def tweetprint():
    if request.method == 'POST':
        keyword = request.form
        keyword = keyword.split(',')
        for x in keyword:
            for tweet in tweepy.cursor(api.search, q = x):
                newTweet = tweets(tweetId=tweet.id,
                                  authorId=tweet.author_id,
                                  content=tweet.text)
                process_status(tweet)
    
    
    return render_template('tweetprint.html', title = "tweetprint page")


# Use when the flask is run from python
if __name__ == "__main__":
    app.run(debug=True)