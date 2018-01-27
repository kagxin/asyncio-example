import asyncio
import time
import sys

OUTTIME = 5
clients = {}


class ProtocolServer(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        clients.setdefault(transport, time.time()+OUTTIME)
        self.transport = transport

    def data_received(self, data):
        message = data.decode('utf8')
        self.transport.write(message)


async def check_alive():
    while True:
        await asyncio.sleep(1)
        for transport, timeout in clients.items():
            if timeout > time.time():
                transport.close()


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    coro = loop.create_server(ProtocolServer, '127.0.0.1', 8888)
    asyncio.ensure_future(check_alive())
    # asyncio.ensure_future(coro)
    try:
        # loop.run_forever(coro)
        loop.run_until_complete(coro)
    except Exception as e:
        print(e)
    finally:
        loop.stop()
        loop.close()

if __name__ == '__main__':
    main()




