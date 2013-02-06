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
import simplejson

from network import Network
from user import User
from http import post, get
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
      self.api = self.IdenticaAPI(self.user.access_key, self.user.access_secret)
      return True
    else:
      logm("A problem has occurred while getting access to Identi.ca API")
      return False
    
  class Oauth:
    def __init__(self):
      self.request_token_url  = 'https://identi.ca/api/oauth/request_token'
      self.access_token_url   = 'https://identi.ca/api/oauth/access_token'
      self.authorize_url      = 'https://identi.ca/api/oauth/authorize'

      consumer_key, consumer_secret = read_consumer_key_and_secret("identica")
      self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
      self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
      
    def get_authorization_url(self):
      self.request_token = self.get_unauthorized_request_token()
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                                                                 token = self.request_token,
                                                                 http_url = self.authorize_url)
      oauth_request.sign_request(self.signature_method, self.consumer, self.request_token)
      return oauth_request.to_url()

    def get_unauthorized_request_token(self):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_method="POST", callback="oob", parameters={"source": "Cairo-Dock"}, http_url = self.request_token_url)
      oauth_request.sign_request(self.signature_method, self.consumer, None)
      url = oauth_request.to_url()
      header = oauth_request.to_header()
      response = post(url, "", header)
      token = oauth.OAuthToken.from_string(response)
      return token
      
    # Exchange request token for access token
    def get_access_token_and_secret(self, pin):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(oauth_consumer=self.consumer, 
            token = self.request_token,  
            http_method="POST",
            callback="oob",
            verifier = pin,
            parameters={"oauth_verifier": str(pin), "source": "Cairo-Dock"},
            http_url=self.access_token_url)

      oauth_request.sign_request(self.signature_method, self.consumer, self.request_token)
      url = oauth_request.to_url()
      header = oauth_request.to_header()
      response = post(url, "", header)
      access_token = oauth.OAuthToken.from_string(response)
      return access_token.key, access_token.secret
      
  class IdenticaAPI():
    def __init__(self, access_key, access_secret):
      self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
      consumer_key, consumer_secret = read_consumer_key_and_secret("identica")
      self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
      self.access_token = oauth.OAuthToken(access_key, access_secret)
      
      self.update_url         = 'http://identi.ca/api/statuses/update.json'
      self.home_timeline_url  = 'http://identi.ca/api/statuses/home_timeline.json'

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
    # twitter is not going to allow, and a error 401 is thrown.
    def tweet(self, message):                                                           # popularly "send a tweet"
      try:
        self.dispatch(self.update_url, "POST", {'status':message})
      except HTTPError as err: # urllib2
        if err.code == 401:
          return False
      else:
        return True
      
    def home_timeline(self):
      return self.dispatch(self.home_timeline_url, "GET")
