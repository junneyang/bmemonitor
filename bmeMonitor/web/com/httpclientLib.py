#-*- coding: utf-8 -*-
#!/usr/bin/env python
import httplib
import urllib
import json

class httpclientLib(object):
    def __init__(self, ip_port, url, method="POST", params=None):
        self.ip_port = ip_port
        self.url = url
        self.method = method
        self.params = params
    def request(self):
        try:
            conn = httplib.HTTPConnection(self.ip_port)
            headers = {"Content-type":"application/json","Connection":"Keep-Alive"}
            if(self.params != None):
                conn.request(self.method, self.url, urllib.urlencode(self.params), headers)
            else:
                conn.request(self.method, self.url, None, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return response.status,json.loads(data)
        except Exception as e:
            return -1,None


if __name__ == "__main__":
    ip_port="tsm.nuomi.com"
    params = {
                "ip":"202.108.23.50"
    }
    url="/tsmdata/goods/iptocityid"
    h = httpclientLib(ip_port, url, method="POST", params=params)
    status,data = h.request()
    print status
    print json.dumps(data, ensure_ascii=False)
