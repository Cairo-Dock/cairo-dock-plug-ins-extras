#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

from oauth import oauth
import simplejson, threading
try:  # python 3
  import urllib.request, urllib.error
  urllib_request = urllib.request
  urllib_error = urllib.error
except:  # python 2
  import urllib2, urllib
  urllib_request = urllib2
  urllib_error = urllib2

from network import Network
from user import User
from http import post, get #, stream
from util import *

class Twitter(Network):
  def __init__(self):
    Network.__init__(self, "twitter")
    self.user = User(network=self.name)
    self.auth = self.Oauth()
    self.api = None
    
  def get_api(self, stream_api_callback):
    if self.user.exists():
      logp("User '%s' found for Twitter" % self.user.screen_name)
      logp("Getting Twitter API")
      self.TwitterStreamAPI(self.user.access_key, self.user.access_secret, stream_api_callback)
      self.api = self.TwitterAPI(self.user.access_key, self.user.access_secret)
      return True
    else:
      logm("A problem has occurred while getting access to Twitter API")
      return False
      
  class Oauth():
    def __init__(self):
      self.request_token_url  = 'https://twitter.com/oauth/request_token'
      self.access_token_url   = 'https://twitter.com/oauth/access_token'
      self.authorize_url      = 'https://twitter.com/oauth/authorize'

      consumer_key, consumer_secret = read_consumer_key_and_secret("twitter")
      self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
      self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

      self.request_token = None
      self.access_token = None
      
    def get_authorization_url(self):
      self.request_token = self.get_unauthorized_request_token()
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                                                                 token = self.request_token,
                                                                 http_url = self.authorize_url)
      oauth_request.sign_request(self.signature_method, self.consumer, self.request_token)
      return oauth_request.to_url()

    def get_unauthorized_request_token(self):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_url = self.request_token_url)
      oauth_request.sign_request(self.signature_method, self.consumer, None)
      url = oauth_request.to_url()
      response = get(url)
      token = oauth.OAuthToken.from_string(response)
      return token

    # Exchange request token for access token
    def get_access_token_and_secret(self, pin):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                                                                 http_url = self.access_token_url,
                                                                 verifier = pin,
                                                                 token = self.request_token)
      oauth_request.sign_request(self.signature_method, self.consumer, self.request_token)
      url = oauth_request.to_url()
      response = get(url)
      self.access_token = oauth.OAuthToken.from_string(response)                      # create both .key and .secret attributes
      return self.access_token.key, self.access_token.secret
      
  class API():
    def __init__(self, access_key, access_secret):
      self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
      consumer_key, consumer_secret = read_consumer_key_and_secret()
      self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
      self.access_token = oauth.OAuthToken(access_key, access_secret)

  class TwitterStreamAPI(API):
    def __init__(self, access_key, access_secret, callback):
      Twitter.API.__init__(self, access_key, access_secret)

      self.user_stream_url = "https://userstream.twitter.com/1.1/user.json"
      self.callback = callback                                                        # called as soon as a new entry on the stream appears
      thread = threading.Thread(target=self.tweet_streaming)                          # keep checking for new entries on the stream
      thread.start()                                                                  # run, forrest run

    def tweet_streaming(self):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                                                                 token = self.access_token,
                                                                 http_url = self.user_stream_url)
      oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)

      url = oauth_request.to_url()
      try:
        req = urllib_request.urlopen(url)
      except urllib_error.URLError:
        return  # we should give the information back to the applet...
      
      buffer = ''
      while True:
        chunk = req.read(1)                                             # read character per character from the connection ...
        if not chunk:
          break

        buffer += chunk
        tweets = buffer.split("\n",1)                                   # ... until find the end of a tweet marked with a '\n'
        if len(tweets) > 1:
          content = tweets[0]
          if "text" in content:
            try:
              content = simplejson.loads(content)
              logp("Received from Twitter Stream: %s" % content)
              self.callback(content)                                    # callback == Twitter.on_receive_new_entry_into_stream_callback
            except ValueError:                                          # in some strange circumstances the content may not be a valid json 
              pass
          buffer = tweets[1]
   
  class TwitterAPI(API):
    def __init__(self, access_key, access_secret):
      Twitter.API.__init__(self, access_key, access_secret)
      
      self.update_url               = 'https://api.twitter.com/1.1/statuses/update.json'
      self.home_timeline_url        = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
      self.direct_messages_url      = 'https://api.twitter.com/1.1/direct_messages.json'
      self.new_direct_messages_url  = 'https://api.twitter.com/1.1/direct_messages/new.json'
      self.verify_credentials_url   = 'https://api.twitter.com/1.1/account/verify_credentials.json'
      self.user_timeline_url        = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
      self.retweet_url_prefix       = 'https://api.twitter.com/1.1/statuses/retweet/'            # lacks the id of the tweet to be retweeted
      
    def dispatch(self, url, mode, parameters={}):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                                                               token = self.access_token,
                                                               http_url = url,
                                                               parameters = parameters,
                                                               http_method = mode)
      oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
      if mode == "GET":
        url = oauth_request.to_url()
        response = get(url) 
        return simplejson.loads(response)
      elif mode == "POST":
        header = oauth_request.to_header()
        post(url, parameters, header)  

    # If an user tries to post the same tweet twice on a short period of time,
    # twitter is not going to allow, and a error 403 is thrown.
    def tweet(self, message):                                                              # popularly "send a tweet"
      try:
        self.dispatch(self.update_url, "POST", {'status':message})
      except urllib_error.HTTPError as err:
        if err.code == 403:
          return False
      else:
        return True
      
    def retweet(self, tweet_id):
      url = "%s%s.json" % (self.retweet_url_prefix, tweet_id)
      self.dispatch(url, "POST")

    def new_direct_message(self, message, destinatary):
      self.dispatch(self.new_direct_messages_url, "POST", {'text':message, 'screen_name':destinatary})

    def home_timeline(self):
      return self.dispatch(self.home_timeline_url, "GET")
    
    def user_timeline(self):
      return self.dispatch(self.user_timeline_url, "GET")

    def direct_messages(self):
      return self.dispatch(self.direct_messages_url, "GET")

    def verify_credentials(self):
      return self.dispatch(self.verify_credentials_url, "GET")
