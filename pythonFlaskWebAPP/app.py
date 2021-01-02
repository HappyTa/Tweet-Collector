from flask import Flask, render_template, url_for, flash, redirect
from forms import keywordRequestForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7c4387868ee2c40bf5aecb48d5e7be09c7c9a142f5ead60c8c267780a94cbdbb'

tweet = [
    {
        'username': 'person 1',
        'content': 'Pizza is flatbread with marinara',
        'date_tweeted': 'April 20,2020'
    },
    {
        'username': 'person 2',
        'content': 'Pizza is flatbread with marinara and cheese',
        'date_tweeted': 'March 20,2020'
    }
]

# A route for the homepage
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = keywordRequestForm()
    if form.validate_on_submit():
        flash(f'keyword(s) recieved {form.keyword.data}!', 'success')
        return redirect(url_for('tweetprint'))
    return render_template('home.html', title = "Home page", form=form)

# About page
@app.route("/tweetprint")
def tweetprint():
    return render_template('tweetprint.html', title = "tweetprint page")


# Use when the flask is run from python
if __name__ == "__main__":
    app.run(debug=True)