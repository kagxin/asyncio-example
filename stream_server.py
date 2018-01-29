"""
官方给的例子, 少加修改:
https://docs.python.org/3/library/asyncio-stream.html
18.5.5.7.4 Register an open socket to wait for data using streams
这个例子也很有趣
"""
import asyncio

async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        if not message:  # 客户端异常
            writer.close()
            break
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8881, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()