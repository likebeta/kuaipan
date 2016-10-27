#!/usr/bin/python
# coding=utf8

import web
import kuaipan

urls = (
    '/files/(.*\.mp3)', 'download_mp3',
    '/(.*)', 'redirect'
)


class download_mp3(object):
    def GET(self, path):
        kp = kuaipan.KuaiPan()
        return web.webapi.found(kp.get_download_url(path.encode('utf8')))


class redirect(object):
    def GET(self, path):
        # return 'bad url: ' + path
        return web.notfound()


app = web.application(urls, globals())
application = app.wsgifunc()
