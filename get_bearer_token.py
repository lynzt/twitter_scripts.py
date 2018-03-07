import os
import base64
import requests

uri = 'https://api.twitter.com/oauth2/token'
consumer_key = os.environ['TWITTER_CONSUMER_KEY'];
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
consumer_key_and_secret = '{0}:{1}'.format(consumer_key, consumer_secret)


bearer_token_credentials = base64.urlsafe_b64encode(consumer_key_and_secret.encode('ascii')).decode('ascii')
body = {'grant_type': 'client_credentials'}
headers = {'Authorization': 'Basic {0}'.format(bearer_token_credentials),
           'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

r = requests.post(uri, data=body, headers = headers)

print (r.text)
