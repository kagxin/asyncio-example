import asyncio
from asyncio import Lock, Event, Condition, Semaphore
import aiohttp
import functools

async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

async def test(loop):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://github.com/kagxin')
        print("html len:{}, loop time:{}".format(len(html), loop.time()))


def main():
    """发起一个http请求"""
    loop = asyncio.get_event_loop()
    print('loop start time:{}'.format(loop.time()))

    try:
        loop.run_until_complete(test(loop))
    finally:
        loop.close()

def main_lock():
    """有三个协程，但一时间之允许有一个协程http请求"""
    """
        locked() 锁是否已经别获取,如果已经被获取，return True
        COROUTINE acquire()  阻塞直到获取锁
        release()  释放锁
        和threding中的Lock一样实现了上下文管理器协议
        with (await lock)  or  with (yield from lock)
    """
    loop = asyncio.get_event_loop()
    print('loop start time:{}'.format(loop.time()))
    lock = Lock()  # lock保证同一时间只有一个，http请求
    async def test(loop, lock, flag):
        with (await lock):  # 试图夺取锁，获得锁之后，执行with块内容，然后释放锁
            async with aiohttp.ClientSession() as session:
                html = await fetch(session, 'http://github.com/kagxin')
                print("html len:{}, flag:{}, loop time:{}".format(len(html), flag, loop.time()))
    
    gs = asyncio.gather(*[test(loop, lock, f) for f in range(3)])
    try:
        loop.run_until_complete(gs)
    finally:
        loop.close()
    """
    (py3env) λ python sync_primitive.py
    loop start time:4209.374
    html len:84032, flag:1, loop time:4211.512
    html len:84032, flag:0, loop time:4217.237
    html len:84032, flag:2, loop time:4220.123
    """

def main_sem():
    """有三个协程，但一时间之允许有一个协程http请求"""
    loop = asyncio.get_event_loop()
    print('loop start time:{}'.format(loop.time()))
    sem = Semaphore(1)  # 信号量值为1的信号量，同一时间只有一个，http请求

    async def test(loop, sem, flag):
        await sem.acquire()  # 试图夺取信号量
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'http://github.com/kagxin')
            print("html len:{}, flag:{}, loop time:{}".format(len(html), flag, loop.time()))
        sem.release()

    gs = asyncio.gather(*[test(loop, sem, f) for f in range(3)])
    try:
        loop.run_until_complete(gs)
    finally:
        loop.close()
    """
        (py3env) λ python sync_primitive.py
        loop start time:4654.726
        html len:84033, flag:2, loop time:4657.534
        html len:84025, flag:1, loop time:4662.043
        html len:84033, flag:0, loop time:4665.038
    """

def main_event():
    """使用event 使协程3秒后进行http请求"""
    """
        clear() reset the internal flag to  False
        is_set() return True if and only if the internal flag is true.
        set() 置位flag，所有wait 都会被唤醒
        COROUTINE wait() 阻塞直到flag置位
    """
    loop = asyncio.get_event_loop()
    print('loop start time:{}'.format(loop.time()))
    event = Event()  # 获取一个event对象

    async def test(loop, event):
        await event.wait()  # 等待set置位
        print("evnet set flag:{}".format(loop.time()))
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'http://github.com/kagxin')
            print("html len:{}, loop time:{}".format(len(html), loop.time()))
        loop.stop()  # 停止事件循环

    set_event_flag = lambda e:e.set()  # event置位函数
    loop.call_later(3, set_event_flag, event)  # 3s 之后置位event
    try:
        loop.run_until_complete(test(loop, event))
    finally:
        loop.close()
    """
        (py3env) λ python sync_primitive.py
        loop start time:5029.55
        evnet set flag:5032.545
        html len:84033, loop time:5034.807
    """

def main_condition():
    """有三个协程，但一时间之允许有一个协程http请求,且保证最先发起http请求的是flag为2的协程"""
    """
        acquire() 获取原始锁
        release() 释放原始锁
        notify(n=1) 唤醒正在wait的n个协程,并释放原始锁
        locked() 原始锁是否已经被获取，如果已经别获取 return True
        notify_all() 唤醒所有正在wait的协程,不释放原始锁
        COROUTINE wait() 释放原始锁,并挂起当前协程
    """
    loop = asyncio.get_event_loop()
    print('loop start time:{}'.format(loop.time()))
    condition = Condition()  # 获取一个Condition对象

    async def test(loop, condition, flag):
        await condition.acquire()  # 获取原始锁
        if flag != 2:  # 让flag为2的协程，先进行http请求
            await condition.wait()  # 释放原始锁,等待被唤醒

        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'http://github.com/kagxin')
            print("html len:{}, flag:{}, loop time:{}".format(len(html), flag, loop.time()))

        condition.notify(n=1)  # 通知激活另外一个协程
        condition.release()  # 释放原始锁


    pt = functools.partial(test, loop, condition)
    gs = asyncio.gather(*map(pt, range(3)))
    try:
        loop.run_until_complete(gs)
    finally:
        loop.close()
    """
        (py3env) λ python sync_primitive.py
        loop start time:9947.637
        html len:84036, flag:2, loop time:9950.086  ## flag为2的协程最先执行
        html len:84035, flag:0, loop time:9952.13
        html len:84035, flag:1, loop time:9954.08
    """


if __name__ == '__main__':
    main_condition()