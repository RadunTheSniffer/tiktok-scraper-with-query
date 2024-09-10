from flask import Flask, request, jsonify, render_template
import tweepy
import snscrape.modules.twitter as sntwitter

app = Flask(__name__)

# Tweepy credentials
api_key = 'YOUR_API_KEY'
api_secret_key = 'YOUR_API_SECRET_KEY'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
api = tweepy.API(auth)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape_tweepy', methods=['POST'])
def scrape_tweepy():
    username = request.form['username']
    count = int(request.form['count'])
    tweets = api.user_timeline(screen_name=username, count=count)
    tweet_data = [{'username': tweet.user.screen_name, 'date': tweet.created_at, 'text': tweet.text} for tweet in tweets]
    return jsonify(tweet_data)

@app.route('/scrape_snscrape', methods=['POST'])
def scrape_snscrape():
    username = request.form['username']
    count = int(request.form['count'])
    tweets = []
    for tweet in sntwitter.TwitterUserScraper(username).get_items():
        if len(tweets) == count:
            break
        tweets.append({'username': tweet.user.username, 'date': tweet.date, 'text': tweet.content})
    return jsonify(tweets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
