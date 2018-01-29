import asyncio

async def receive(reader, writer):
    while True:
        data = await reader.read(1024)  # 接收数据
        loop = asyncio.get_event_loop()
        print('[{}][received] {}'.format(loop.time(), data.decode()), flush=True)

async def send(reader, writer):
    while True:
        writer.write('hello world'.encode())
        await writer.drain()  # 等待写入数据
        await asyncio.sleep(2)
    

loop = asyncio.get_event_loop()
loop.set_debug(True)
reader, writer = loop.run_until_complete(asyncio.open_connection('127.0.0.1', 8881, loop=loop))  # 连接服务端，拿到stream
asyncio.ensure_future(receive(reader, writer))
asyncio.ensure_future(send(reader, writer))

try:
    loop.run_forever()
except Exception as e:
    print(str(e))
finally:
    loop.stop()
    loop.close()