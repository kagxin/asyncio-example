import asyncio
from functools import partial
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.DEBUG)

async def hello_world1():
    while True:
        print('hello_wrold1')
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:  #捕获删除协程的exception, 跳出while
            break

async def hello_world2():
    while True:
        print('hello_world2')
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            break


def del_task(*tasks):  # 删除掉tasks
    for task in tasks:
        task.cancel()


loop = asyncio.get_event_loop()
loop.set_debug(True)  # 打开debug模式

task1 = asyncio.ensure_future(hello_world1())  # 把helloworld协程加入task调度
task2 = asyncio.ensure_future(hello_world2())
loop.call_at(loop.time()+5, del_task, task1, task2)  # 5s之后删除两个helloworld协程

try:
    loop.run_until_complete(asyncio.gather(task1, task2))  #等待两个协程结束
finally:
    loop.stop()
    loop.close()



