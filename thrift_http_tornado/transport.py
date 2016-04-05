import cStringIO
import logging

import toro
import thrift.transport.TTransport
import tornado.gen
import tornado.ioloop
import tornado.httpclient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class THTTPTornadoTransport(thrift.transport.TTransport.TTransportBase):
    def __init__(self, endpoint_url='http://localhost:8989',
                 io_loop=None, *args, **kwargs):
        self._client = tornado.httpclient.AsyncHTTPClient()
        self._wbuf = cStringIO.StringIO()
        self.io_loop = io_loop or tornado.ioloop.IOLoop.instance()
        self._endpoint = endpoint_url
        self._response_queue = toro.Queue(io_loop=self.io_loop)
        self._kwargs = kwargs
        self._headers = {'Content-Type': 'application/x-thrift'}

    def open(self, *args, **kwargs):
        pass

    @tornado.gen.coroutine
    def readFrame(self):
        result = yield self._response_queue.get()

        if 'error' in result:
            raise result['error']
        else:
            raise tornado.gen.Return(result['response'])

    def close(self):
        pass

    def isOpen(self):
        return True

    def read(self, _):
        assert False, "wrong stuff"

    def write(self, buf):
        self._wbuf.write(buf)

    @tornado.gen.coroutine
    def flush(self):
        self.fetch(self._wbuf.getvalue())
        self._wbuf = cStringIO.StringIO()

    @tornado.gen.coroutine
    def fetch(self, buf):
        request = tornado.httpclient.HTTPRequest(
            url=self._endpoint, headers=self._headers, method="POST", body=buf,
            **self._kwargs)

        try:
            r = yield self._client.fetch(request)

            self._response_queue.put({'response': r.body})
        except Exception as e:
            self._response_queue.put({'error': e})
