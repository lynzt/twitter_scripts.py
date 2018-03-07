import os
import sys
import json
import urllib
import base64
import requests

def search_twitter(next_token):
    uri = 'https://api.twitter.com/1.1/tweets/search/30day/dev.json'
    bearer_token = os.environ['TWITTER_BEARER_TOKEN']

    query_string = {'query': 'to:BetsyHodges has:images', 'maxResults': '100', 'fromDate': '201802180000', 'toDate': '201802210000'}
    if next_token != '' and next_token != 'start':
        query_string['next'] = next_token
    headers = { 'Authorization': 'Bearer {}'.format(bearer_token) }

    r = requests.get(uri, params=query_string, headers = headers)
    return r.json()

def get_tweets(json_results):
    if 'next' in json_results:
        next_token = json_results['next']
    else:
        next_token = ''
    results = json_results['results']

    tweet_replies = list(filter(lambda x: x['in_reply_to_status_id'] == 965306743986278401, results))
    return {'next_token': next_token, 'tweet_replies': tweet_replies}

def process_results(tweets):
    print ('nbr tweets: {}'.format(len(tweets)))

    for tweet in tweets:
        screen_name = tweet['user']['screen_name']
        print("processing: {}".format(screen_name))
        media = get_extended_entities(tweet)
        if media:
            images = list(filter(lambda x: x['type'] == 'photo', media))
            for idx, image in enumerate(images):
                if idx == 0:
                    urllib.request.urlretrieve(image['media_url'], './images/{}.jpg'.format(screen_name))
                else:
                    urllib.request.urlretrieve(image['media_url'], './images/{}{}.jpg'.format(screen_name, idx))

def get_extended_entities(tweet):
    if 'extended_entities' in tweet:
        return tweet['extended_entities']['media']
    else:
        return None

def main():
    next_token = 'start'
    counter = 0
    tweets = []
    while(next_token):
        print('searching tweets: {}'.format(counter))
        counter += 1
        json_results = search_twitter(next_token)
        results = get_tweets(json_results)
        next_token = results['next_token']
        tweets += results['tweet_replies']
        if counter > 10:
            break;

    process_results(tweets)


if __name__ == '__main__':
    main()
