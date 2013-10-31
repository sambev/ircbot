import sys
import urllib2
import urllib
import httplib
from xml.etree import ElementTree as etree
 
class wolfram(object):
    def __init__(self, appid):
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent':None}
 
    def _get_xml(self, question):
        url_params = {'input':question, 'appid':self.appid}
        data = urllib.urlencode(url_params)
        #print data
        req = urllib2.Request(self.base_url, data, self.headers)
        #print req
        xml = urllib2.urlopen(req).read()
        return xml
 
    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        #retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag=='subpod']:
                for it in [i for i in list(item) if i.tag=='plaintext']:
                    if it.tag=='plaintext':
                        data_dics[e.get('title')] = it.text
        return data_dics
 
    def search(self, question):
        xml = self._get_xml(question)
        response = self._xmlparser(xml)
        return response
 
if __name__ == "__main__":
    appid = sys.argv[1]
    query = sys.argv[2]
    w = wolfram(appid)
    print w.search(query)
