import sys
sys.path.append('gen-py.tornado')
from tornado import ioloop, gen
io_loop = ioloop.IOLoop.instance()
from scrapper import Scrapper
from thrift.protocol import TJSONProtocol
from thrift_http_tornado import THTTPTornadoTransport


@gen.coroutine
def communicate():
    transport = THTTPTornadoTransport()
    pfactory = TJSONProtocol.TJSONProtocolFactory()
    client = Scrapper.Client(transport, pfactory)

    futures = [client.scrape('http://google.com/') for i in xrange(100)]

    yield futures

    io_loop.stop()

io_loop.add_callback(communicate)
io_loop.start()
