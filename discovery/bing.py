import myparser
import time
import http.client
import sys


class BingSearch:
    def __init__(self, word, limit, offset):
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.server = "www.bing.com"
        self.apiserver = "api.search.live.net"
        self.hostname = "www.bing.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "50"
        self.limit = int(limit)
        self.bingApi = ""
        self.counter = offset

    def do_search(self):
        h = http.client.HTTPConnection(self.server)
        h.putrequest('GET', "/search?q=%40" + self.word + "&count=50&first=" + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader('Cookie: SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50')
        h.putheader('Accept-Language: en-us,en')
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        response = h.getresponse()
        self.results = str(response.read())
        self.totalresults += self.results

    def do_search_api(self):
        h = http.client.HTTPConnection(self.apiserver)
        h.putrequest('GET',
                     "/xml.aspx?Appid=" + self.bingApi + "&query=%40" + self.word + "&sources=web&web.count=40&web.offset=" + str(
                         self.counter))
        h.putheader('Host', "api.search.live.net")
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        response = h.getresponse()
        self.results = str(response.read())
        self.totalresults += self.results

    def do_search_vhost(self):
        h = http.client.HTTPConnection(self.server)
        h.putrequest('GET', "/search?q=ip:" + self.word + "&go=&count=50&FORM=QBHL&qs=n&first=" + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader('Cookie: mkt=en-US;ui=en-US;SRCHHPGUSR=NEWWND=0&ADLT=DEMOTE&NRSLT=50')
        h.putheader('Accept-Language: en-us,en')
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        response = h.getresponse()
        self.results = str(response.read())
        self.totalresults += self.results

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_allhostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames_all()

    def process(self, api):
        if api == "yes":
            if self.bingApi == "":
                print("Please insert your API key in the discovery/bing.py")
                sys.exit()
        while self.counter < self.limit:
            if api == "yes":
                self.do_search_api()
                time.sleep(0.3)
            else:
                self.do_search()
                time.sleep(1)
            self.counter += 50
            print("\tSearching " + str(self.counter) + " results...")

    def process_vhost(self):
        while self.counter < self.limit:  # Maybe it is good to use other limit for this.
            self.do_search_vhost()
            self.counter += 50
