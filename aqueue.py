"""
IF:
    asyncio ImportError: cannot import name 'Full'
THEN:
    Check if your project or current working directory includes a file called queue.py and rename it. 
"""

import asyncio

async def produce(queue, num):
    for i in range(num):
        await queue.put('hello')  # 队列中加入
        await asyncio.sleep(1)
    await queue.put(None)


async def consume(queue):
    while True:
        res = await queue.get()  # 取数据
        if res is None:
            break
        print('consume:{}'.format(res))


def main():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    try:
        loop.run_until_complete(asyncio.gather(
            produce(queue, 5),
            consume(queue)
        ))
    except Exception as e:
        print(str(e))
    finally:
        loop.stop()
        loop.close()

if __name__ == '__main__':
    main()
