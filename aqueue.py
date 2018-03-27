"""
IF:
    asyncio ImportError: cannot import name 'Full'
THEN:
    Check if your project or current working directory includes a file called queue.py and rename it. 
"""

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.DEBUG)

async def produce(queue, num):
    for i in range(num):
        await queue.put(i)  # 队列中加入
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
    loop.set_debug(True)
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
