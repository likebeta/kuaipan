#!/usr/bin/python
#coding=utf8

import urllib 
import hmac
import hashlib
import base64
import time
import random

class signature:
	def __init__(self,baseUrl,oauth_consumer_key,consumer_secret,oauth_token='',oauth_token_secret='',httpMethod="GET"):
		self.consumer_key=oauth_consumer_key
		self.consumer_secret=consumer_secret
		self.oauth_token=oauth_token
		self.oauth_token_secret=oauth_token_secret
		self.http_method=httpMethod
		self.baseUrl=baseUrl
		self.queryString=[]

	def createDict(self,kvs):
		if not kvs.has_key('oauth_consumer_key') :
			kvs["oauth_consumer_key"]=self.consumer_key
		if not kvs.has_key('oauth_token') and len(self.oauth_token)>0:
			kvs["oauth_token"]=self.oauth_token
		if not kvs.has_key('oauth_signature_method'):
			kvs["oauth_signature_method"]="HMAC-SHA1"
		if not kvs.has_key("oauth_timestamp"):
			kvs["oauth_timestamp"]=str(int(time.time()))
		if not kvs.has_key('oauth_nonce'):
			kvs["oauth_nonce"]=str(int(time.time()))+str(random.randint(100,999)) #13
		if not kvs.has_key("oauth_version"):
			kvs['oauth_version']='1.0'
		signValue="%s&%s&%s" % (self.http_method,urllib.quote_plus(self.baseUrl), urllib.quote_plus(self.dict2string(kvs)))
		#print signValue
		kvs["oauth_signature"]=self.encry(signValue)
		self.kvs=kvs 
		#print self.kvs 
		
	def dict2string(self,kvs):
		self.queryString=[urllib.quote_plus(k)+"="+urllib.quote_plus(v) for k,v in kvs.items()]
		self.queryString.sort()
		return "&".join(self.queryString)

	def encry(self,word):
		myhmac=hmac.new(self.consumer_secret+"&"+self.oauth_token_secret,digestmod=hashlib.sha1)
		myhmac.update(word)
		signStr=base64.encodestring( myhmac.digest())
		return urllib.quote_plus(signStr.strip())

	def geturl(self):
		return self.baseUrl+"?"+"&".join([k+"="+v for k,v in self.kvs.items()])

if __name__ == "__main__":
	myKey='xczbJ2JdwFjf4Fug'
	mySec='P5oLZMrovwJqJyfu'
	myUrl='https://openapi.kuaipan.cn/open/requestToken'
	myTest=signature(myUrl,myKey,mySec)
	myTest.createDict({})
	print myTest.geturl()
