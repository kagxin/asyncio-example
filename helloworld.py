import asyncio
import functools
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.DEBUG)

def hello_wrold(loop, arg):
    print(arg)
    loop.stop()


def main():
    loop = asyncio.get_event_loop()   # 获取事件循环
    loop.set_debug(True)  # 打开debug模式
    # loop.call_soon(hello_wrold, loop, 'hello world!')  
    loop.call_soon(functools.partial(hello_wrold, loop=loop, arg='hello world!'))  # 向事件循环中注册回调函数，使用偏函数，显示keyword
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()