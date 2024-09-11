from flask import Flask, request, jsonify, render_template
import snscrape.modules.twitter as sntwitter
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape_snscrape', methods=['POST'])
def scrape_snscrape():
    keyword = request.form['keyword']
    count = int(request.form['count'])
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f'{keyword}').get_items():
        if len(tweets) == count:
            break
        tweets.append({
            'username': tweet.user.username,
            'date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
            'text': tweet.content
        })
    
    # Sort tweets by date
    tweets.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    
    return render_template('results.html', tweets=tweets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

