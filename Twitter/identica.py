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
import urllib2, urllib

from user import User
from http import post, get
from util import *

class Identica:
  def __init__(self):
    self.name = "identica"
    self.user = User(network=self.name)
    
  def get_api(self):
    if self.user_exists():
      logp("Getting Identi.ca API")
      return self.IdenticaAPI(self.user.access_key, self.user.access_secret)
    else:
      return False
      
  def user_exists(self):
    return self.user.access_secret and self.user.access_secret
    
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
      print "=================="
      print self.access_token
      print "=================="
      
      self.update_url = 'http://identi.ca/api/statuses/update.json'

    def dispatch(self, url, mode, parameters={}):
      oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                                                               token = self.access_token,
                                                               http_url = url,
                                                               parameters = parameters,
                                                               http_method = mode)
      oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
      print oauth_request.to_url()
      if mode == "GET":
        url = oauth_request.to_url()
        response = get(url) 
        return simplejson.loads(response)
      elif mode == "POST":
        header = oauth_request.to_header()
        post(url, parameters, header)  

    def tweet(self, message):                                                                 # popularly "send a tweet"
      self.dispatch(self.update_url, "POST", {'status':message})
