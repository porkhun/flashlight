from __future__ import print_function
import logging

from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.options import options, define

from models import FlashlightManager


define("host", default="127.0.0.1", help="TCP server host")
define("port", default=9999, help="TCP port to connect to")

logger = logging.getLogger(__name__)
flashlight_manager = FlashlightManager()


class Client(TCPClient):
    connection_retry_time = 6

    @gen.coroutine
    def run(self, host, port):
        while True:
            try:
                stream = yield self.connect(host, port)
                logger.debug('Connection established')
                stream.set_nodelay(True)

                while True:
                    # read type
                    data_type = yield stream.read_bytes(1)
                    # read length
                    data_length = yield stream.read_bytes(2)
                    data_value = None
                    if data_length:
                        data_value = yield stream.read_bytes(data_length)
                    flashlight_manager.handle_command(data_type, data_value)
            except StreamClosedError as exc:
                logger.error("Error connecting to %d: %s", port, exc)
                yield gen.sleep(self.connection_retry_time)


if __name__ == '__main__':
    options.parse_command_line()
    Client().run(options.host, options.port)
    logger.debug('Connecting to server socket...')
    IOLoop.instance().start()
    logger.debug('Socket has been closed.')
