#!/usr/bin/python
#coding=utf8

import signature
import json
import time
import urllib
import urllib2
import random, string

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
		d = {}
		d['oauth_consumer_key'] = self.oauth_consumer_key
		d['oauth_consumer_secret'] = self.oauth_consumer_secret
		d['oauth_token'] = self.oauth_token
		d['oauth_token_secret'] = self.oauth_token_secret
		d['charged_dir'] = self.charged_dir
		d['user_id'] = self.user_id
		s = json.dumps(d)
		with open('kuaipan_token.json','w') as f:
			f.write(s)
		return True

	def list(self):
		pass

	def get_download_url(self,path):
		baseurl = 'http://api-content.dfs.kuaipan.cn/1/fileops/download_file'
		s = signature.signature(baseurl,self.oauth_consumer_key,self.oauth_consumer_secret,self.oauth_token,self.oauth_token_secret)
		s.createDict({'root':'app_folder','path':path})
		url = s.geturl()
		return url

if __name__ == '__main__':
	kp = kuaipan()
#	kp.auth()
	print kp.get_download_url('当你老了.mp3')
