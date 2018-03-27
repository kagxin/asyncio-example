"""
如果协程的内部，发生的异常没有被消费，在垃圾回收器删除future的时候，会log异常的回溯日志
三种方式去消费一个协程中的异常：
    1、使用run_until_complete: 这个有局限，在协程内部不能使用
    2、在业务协程外包裹一个协程来消费这个异常 例如 例子中的： handle_exception
    3、写一个装饰器，其实就是也就是使用的链式协程消费的异常只不过，协程了装饰器的形式，便于使用
"""

import asyncio
import logging
from functools import wraps
import functools

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


async def handle_exception(task):
    try:
        await task
    except Exception as e:
        logging.exception(str(e))
        print("exception consumed")


def log_asyncio_exception(coro):  # 消费协程异常的装饰器，log 完整堆栈，之后再抛出异常
    async def handle_exception(*args, **kwargs):
        try:
            return await coro(*args, **kwargs)
        except Exception as e:
            logging.exception(str(e))
    return handle_exception

async def test(loop):
    end_time = loop.time() + 5
    while True:
        await asyncio.sleep(1)
        print('hello')
        if loop.time() > end_time:
            break


async def bug():
    raise Exception('test except')

@log_asyncio_exception
async def bug2():
    raise Exception('test 2 except')

def test_dec():
    raise Exception('test except')

loop = asyncio.get_event_loop()
loop.set_debug(True)

asyncio.ensure_future(handle_exception(bug()))  # 使用链式协程消费异常
asyncio.ensure_future(bug2())  # 使用装饰器消费异常

try:
    loop.run_until_complete(test(loop))
except Exception:
    print("exception consumed")
finally:
    loop.stop()
    loop.close()

