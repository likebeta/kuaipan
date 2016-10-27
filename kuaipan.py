#!/usr/bin/python
# coding=utf8

import json
import urllib
import urllib2
import signature
from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler
from poster.streaminghttp import StreamingHTTPSHandler
from poster.streaminghttp import StreamingHTTPRedirectHandler


class KuaiPan(object):
    def __init__(self):
        self.oauth_consumer_key = None
        self.oauth_consumer_secret = None
        with open('kuaipan_token.json') as f:
            data = f.read()
            j = json.loads(data)
            for k, v in j.items():
                setattr(self, str(k), str(v))

    def __requestToken(self):
        baseurl = 'https://openapi.kuaipan.cn/open/requestToken'
        s = signature.Signature(baseurl, self.oauth_consumer_key, self.oauth_consumer_secret)
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
        url = 'https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token=' + self.oauth_token
        print 'please open %s to auth,then pass code here and press enter' % url
        code = int(raw_input("Auth Code: "))
        return True

    def __accessToken(self):
        baseurl = 'https://openapi.kuaipan.cn/open/accessToken'
        s = signature.Signature(baseurl, self.oauth_consumer_key, self.oauth_consumer_secret, self.oauth_token,
                                self.oauth_token_secret)
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
        d = dict()
        d['oauth_consumer_key'] = self.oauth_consumer_key
        d['oauth_consumer_secret'] = self.oauth_consumer_secret
        d['oauth_token'] = self.oauth_token
        d['oauth_token_secret'] = self.oauth_token_secret
        d['charged_dir'] = self.charged_dir
        d['user_id'] = self.user_id
        s = json.dumps(d)
        with open('kuaipan_token.json', 'w') as f:
            f.write(s)
        return True

    def list(self):
        pass

    def get_download_url(self, path):
        baseurl = 'http://api-content.dfs.kuaipan.cn/1/fileops/download_file'
        s = signature.Signature(baseurl, self.oauth_consumer_key, self.oauth_consumer_secret, self.oauth_token,
                                self.oauth_token_secret)
        s.createDict({'root': 'app_folder', 'path': path})
        url = s.geturl()
        return url

    def upload(self, local, remote):
        baseurl = 'http://api-content.dfs.kuaipan.cn/1/fileops/upload_locate'
        s = signature.Signature(baseurl, self.oauth_consumer_key, self.oauth_consumer_secret, self.oauth_token,
                                self.oauth_token_secret)
        s.createDict({})
        url = s.geturl()
        f = urllib.urlopen(url)
        if f.getcode() != 200:
            return False
        data = f.read()
        j = json.loads(data)
        if not j.has_key('url'):
            return False
        baseurl = j['url'] + '1/fileops/upload_file'
        s = signature.Signature(baseurl, self.oauth_consumer_key, self.oauth_consumer_secret, self.oauth_token,
                                self.oauth_token_secret, 'POST')
        s.createDict({'overwrite': 'True', 'root': 'app_folder', 'path': remote})
        opener = urllib2._opener
        if opener is None:
            opener = urllib2.build_opener()
            opener.add_handler(StreamingHTTPHandler())
            opener.add_handler(StreamingHTTPRedirectHandler())
            opener.add_handler(StreamingHTTPSHandler())
        urllib2.install_opener(opener)

        datagen, headers = multipart_encode({"file": open(local, 'rb')})
        headers['Content-Disposition'] = 'form-data; name="file"; filename="test.py"'
        url = s.geturl()
        print url
        request = urllib2.Request(url, datagen, headers)
        print urllib2.urlopen(request).read()

        return True


if __name__ == '__main__':
    kp = KuaiPan()
    # kp.auth()
    print kp.get_download_url('明年 今日.mp3')
    # kp.upload('j.mp3','j.mp3')
