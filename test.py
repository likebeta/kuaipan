#!/usr/bin/python
#coding:utf8

import urllib

a = {}
a['name'] = '易思龙'
a['age'] = 24
a['sign'] = 'kjdlkjd452%40lkjkl'

print a
print urllib.urlencode(a)

print '&'.join([str(k)+'='+str(v) for k,v in a.items()])

s = '&'.join([urllib.quote(str(k))+'='+urllib.quote(str(v)) for k,v in a.items() if k != 'sign' ])
s += '&' + 'sign=' + a['sign']
print s

