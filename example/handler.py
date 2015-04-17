import sys
sys.path.append('gen-py.tornado')

from thrift.protocol import TJSONProtocol
from scrapper import Scrapper
from thrift_http_tornado import THTTPTornadoServer
from tornado import ioloop, gen
from tornado.httpclient import AsyncHTTPClient
http_client = AsyncHTTPClient()
loop = ioloop.IOLoop.instance()


@gen.engine
def fetch_data(url, callback):
    print "done"
    callback(Scrapper.Blog(url='bar', content='foo'))


class ScraperHandler(object):
    def __init__(self):
        pass

    def scrape(self, url):
        return gen.Task(fetch_data, url)

handler = ScraperHandler()
processor = Scrapper.Processor(handler)
pfactory = TJSONProtocol.TJSONProtocolFactory()
server = THTTPTornadoServer(processor, pfactory)

server.start()
loop.start()
