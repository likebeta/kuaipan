#!/usr/bin/python
#coding=utf8

import signature
import json
import time
import urllib
import urllib2
import random, string

def random_str(randomlength=20):
	a = list(string.ascii_letters)
	random.shuffle(a)
	return ''.join(a[:randomlength])

class kuaipan:
	def __init__(self):
		with open('kuaipan_token.json') as f:
			data = f.read()
			j = json.loads(data)
			for k,v in j.items():
				setattr(self,str(k),str(v))

	def __requestToken(self):
		baseurl = 'https://openapi.kuaipan.cn/open/requestToken'
		s = signature.signature(baseurl,self.oauth_consumer_key,self.oauth_consumer_secret)
		s.createDict({})
		url = s.geturl()
		f = urllib.urlopen(url)
		if f.getcode() != 200:
			return False
		data = f.read()
		j = json.loads(data)
		if not j.has_key('oauth_token_secret'):
			return False
		self.oauth_token_secret = str(j['oauth_token_secret'])
		self.oauth_token = str(j['oauth_token'])
		return True

	def __authorize(self):
		url='https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token=' + self.oauth_token
		print('please open %s to auth,then pass code here and press enter'%(url))
		code = (int)(raw_input("Auth Code: "))
		return True

	def __accessToken(self):
		baseurl = 'https://openapi.kuaipan.cn/open/accessToken'
		s = signature.signature(baseurl,self.oauth_consumer_key,self.oauth_consumer_secret,self.oauth_token,self.oauth_token_secret)
		s.createDict({})
		url = s.geturl()
		f = urllib.urlopen(url)
		if f.getcode() != 200:
			return False
		data = f.read()
		j = json.loads(data)
		if not j.has_key('oauth_token_secret'):
			return False

		self.oauth_token_secret = str(j['oauth_token_secret'])
		self.oauth_token = str(j['oauth_token'])
		self.oauth_token_secret = str(j['oauth_token_secret'])
		self.oauth_token = str(j['oauth_token'])
		self.charged_dir = str(j['charged_dir'])
		self.user_id = j['user_id']
		return True

	def auth(self):
		if not self.__requestToken():
			return False
		if not self.__authorize():
			return False
		if not self.__accessToken():
			return False
		return True

	def list(self):
		pass
	def get_download_url(self):
		pass

if __name__ == '__main__':
	kp = kuaipan()
	kp.auth()
