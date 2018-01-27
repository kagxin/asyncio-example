import asyncio
import time

OUTTIME = 10
clients = {}


class ProtocolServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        clients.setdefault(transport, time.time()+OUTTIME)

    def data_received(self, data):
        clients.update({self.transport: time.time()+OUTTIME})  # 一旦接受到数据就更新timeout时间
        message = data.decode()
        self.transport.write(message.encode())


async def check_alive():  # 如果timeout就通过对应的transport将客户端关闭
    while True:
        await asyncio.sleep(0.3)
        for transport, timeout in clients.copy().items():
            if timeout < time.time():
                print(transport, timeout, time.time())
                transport.close()
                clients.pop(transport)


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    coro = loop.create_server(ProtocolServer, '127.0.0.1', 8881)
    asyncio.ensure_future(coro)
    asyncio.ensure_future(check_alive(), loop=loop)

    try:
        loop.run_forever()
    except Exception as e:
        print(e)
    finally:
        loop.stop()
        loop.close()

if __name__ == '__main__':
    main()




