import asyncio

def hello_world(loop):
    print('Hello World')

async def hello():
    while True:
        await asyncio.sleep(1)
        print('hello world')

async def hello2():
    while True:
        await asyncio.sleep(2)
        print('hello world2')


loop = asyncio.get_event_loop()

loop.call_soon(hello_world, loop)

tasks = [
        asyncio.ensure_future(hello2()),
        asyncio.ensure_future(hello()),

    ]

try:
    loop.run_until_complete(asyncio.wait(tasks))
except Exception as e:
    print(e)

loop.close()
