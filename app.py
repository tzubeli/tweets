from flask import Flask, abort, render_template
import os
import requests
import json
import base64
import webbrowser
import math

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file)


@app.route('/tweets/', defaults={'page': 1})
@app.route('/tweets/page/<int:page>', methods=['GET'])
def get_tweets(page):

    authentication = authenticate(config['consumer_key'], config['consumer_secret'])

    if 'access_token' not in authentication:
        abort(404, authentication)

    headers = {
        'Authorization': 'Bearer ' + authentication['access_token']
    }

    params = {
        'q': config['hashtag'],
        'count': config['tweet_count'],
        'result_type': 'recent'
    }
    try:
        response = requests.get(config['search_url'], params=params, headers=headers)
    except Exception:
        abort(500, 'Cannot retrieve tweets')

    if response.status_code != 200:
        abort(500, 'Cannot retrieve tweets: {}'.format(json.loads(response.text)['errors'][0]['message']))

    tweets = json.loads(response.text)

    if len(tweets['statuses']) == 0 or 'statuses' not in tweets:
        abort(404, 'No posts available')

    data = []

    for details in paginated_posts(tweets['statuses'], page):

        user = details['user']
        post = {
            'date': format_date(details.get('created_at', '')),
            'text': details.get('text', ''),
            'screen_name': '@{}'.format(user.get('screen_name', '')),
            'name': user.get('name', ''),
            'image': user.get('profile_image_url', ''),
            'url': 'https://twitter.com/statuses/{}'.format(details.get('id'))
        }
        # remove image url from text
        url = post['text'].find('https')
        if url > -1:
            post['text'] = post['text'][:url]

        data.append(post)

    total_pages = math.ceil(len(tweets['statuses'])/config['page_limit'])
    return render_template('tweets.html', tweets=data, page=page, total=total_pages)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404


@app.errorhandler(500)
def error(error):
    return render_template('error.html', error=error), 500


def format_date(date):
    elements = date.split(' ')
    return '{} {}'.format(elements[1], elements[2])


def authenticate(consumer_key, consumer_secret):

    bearer_token = base64.b64encode('{}:{}'.format(consumer_key, consumer_secret).encode('utf-8'))

    headers = {
        'Authorization': 'Basic ' + bearer_token.decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    data = {'grant_type': 'client_credentials'}

    try:
        authentication = requests.post(config['auth_url'], headers=headers, data=data)
    except Exception:
        abort(500, 'Cannot authenticate.')

    if 'errors' in authentication.text:
        app.logger.error(authentication.text)
        return json.loads(authentication.text)['errors'][0]['message']
    else:
        return json.loads(authentication.text)


def paginated_posts(tweets, page):
    start = config['page_limit'] * (page-1)
    end = min(start + config['page_limit'], len(tweets))
    return tweets[start:end]


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000/tweets/')
    app.run()


