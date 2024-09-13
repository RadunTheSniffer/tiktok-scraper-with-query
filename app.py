from flask import Flask, request, jsonify, render_template
import snscrape.modules.twitter as sntwitter
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape_snscrape', methods=['POST'])
def scrape_snscrape():
    username = request.form.get('username')
    count = request.form.get('count')
    if not username or not count:
        return "Missing username or count", 400
    count = int(count)
    tweets = []
    try:
        for tweet in sntwitter.TwitterSearchScraper(f'from:{username}').get_items():
            if len(tweets) == count:
                break
            tweets.append({
                'username': tweet.user.username,
                'date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
                'text': tweet.content
            })
            time.sleep(1)  # Add a 1-second delay between requests
    except sntwitter.ScraperException as e:
        return f"An error occurred: {e}", 500
    tweets.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    return render_template('results.html', tweets=tweets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

