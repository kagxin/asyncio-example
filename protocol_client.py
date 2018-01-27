import asyncio
import functools


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        message = 'hello world!'
        transport.write(message.encode())
        print('Data sent: {!r}'.format(message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


def main():
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(functools.partial(EchoClientProtocol, loop=loop),
                                  '127.0.0.1', 8881)

    loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except Exception as e:
        print(str(e))
    finally:
        loop.close()

if __name__ == '__main__':
    main()