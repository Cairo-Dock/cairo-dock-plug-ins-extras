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
try:
  from urllib.error import HTTPError
except:
  from urllib2 import HTTPError

from simplejson import loads, dumps

from network import Network
from user import User
from http import post_to_identica, get
from util import *

class Identica(Network):
  def __init__(self):
    Network.__init__(self, "identica")
    self.user = User(network=self.name)
    self.auth = self.Oauth()
    self.api = None
    
  def get_api(self):
    if self.user.exists():
      logp("User '%s' found for Identi.ca" % self.user.screen_name)
      logp("Getting Identi.ca API")
      self.api = self.IdenticaAPI(self.user.access_key, self.user.access_secret, self.user.screen_name)
      return True
    else:
      logm("A problem has occurred while getting access to Identi.ca API")
      return False
    
  class Oauth:
    def __init__(self):
      self.request_token_url  = 'https://identi.ca/oauth/request_token'
      self.access_token_url = 'https://identi.ca/oauth/access_token'
      self.authorize_url = 'https://identi.ca/oauth/authorize'

      consumer_key, consumer_secret = read_consumer_key_and_secret("identica")
      self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
      self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
      
    def get_authorization_url(self):
      self.request_token = self.get_unauthorized_request_token()
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token = self.request_token, http_url = self.authorize_url)
      oauth_request.sign_request(self.signature_method, self.consumer, self.request_token)
      return oauth_request.to_url()

    def get_unauthorized_request_token(self):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_url = self.request_token_url, callback="oob")
      oauth_request.sign_request(self.signature_method, self.consumer, None)
      url = oauth_request.to_url()
      response = get(url)
      token = oauth.OAuthToken.from_string(response)
      return token
      
    # Exchange request token for access token
    def get_access_token_and_secret(self, verifier):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(oauth_consumer=self.consumer, 
                                                                 token = self.request_token,
                                                                 callback="oob",
                                                                 verifier = str(verifier),
                                                                 http_url = self.access_token_url)
      oauth_request.sign_request(self.signature_method, self.consumer, self.request_token)
      url = oauth_request.to_url()
      response = get(url)
      access_token = oauth.OAuthToken.from_string(response)
      return access_token.key, access_token.secret
      
  class IdenticaAPI():
    def __init__(self, access_key, access_secret, user_screen_name):
      self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
      consumer_key, consumer_secret = read_consumer_key_and_secret("identica")
      self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
      self.access_token = oauth.OAuthToken(access_key, access_secret)
      
      self.feed_url = "https://identi.ca/api/user/%s/feed" % user_screen_name

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
        return loads(response)
      elif mode == "POST":
        headers = {'Content-Type': 'application/json'}
        post_to_identica(oauth_request.to_url(), dumps(parameters), headers)

    def tweet(self, message):                                                           # popularly "send a tweet"
      try:
        note = {"verb": "post", "object": {"content": message, "objectType": "note"}}
        self.dispatch(self.feed_url, "POST", note)
      except HTTPError as err: # urllib2
        if err.code == 401:
          return False
      else:
        return True
      
    def home_timeline(self):
      return "Not implemented"
      # return self.dispatch(self.home_timeline_url, "GET")
