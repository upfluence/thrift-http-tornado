import logging

import tornado.gen
import tornado.web
import thrift.transport.TTransport

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class THTTPTornadoHandler(tornado.web.RequestHandler):
    def initialize(self, thrift_server):
        self._thrift_server = thrift_server

    @tornado.gen.coroutine
    def post(self):
        yield self._thrift_server.on_message(self.request.body, self)


class THTTPTornadoServer(object):
    @classmethod
    def build_endpoint(cls, processor, iprot_factory, oprot_factory=None,
                       path="/"):
        srv = cls(processor, iprot_factory, oprot_factory, path=path)

        return (path, THTTPTornadoHandler, dict(thrift_server=srv))

    def __init__(self, processor, iprot_factory, oprot_factory=None, port=8989,
                 path="/", **kwargs):
        self._processor = processor
        self._iprot_factory = iprot_factory
        self._oprot_factory = oprot_factory if oprot_factory else iprot_factory
        self._port = port
        self._path = path
        self._application = tornado.web.Application([
            (path, THTTPTornadoHandler, dict(thrift_server=self)),
        ])

    def start(self):
        self._application.listen(self._port)

    @tornado.gen.coroutine
    def on_message(self, body, writer):
        iprot = self._iprot_factory.getProtocol(
            thrift.transport.TTransport.TMemoryBuffer(body))

        oprot = self._oprot_factory.getProtocol(writer)

        yield self._processor.process(iprot, oprot)
