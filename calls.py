import asyncio
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.DEBUG)

def hello_world():
    print(datetime.datetime.now(), ' ', end='')
    print('Hello World')


def print_delay(arg, handle):
    print(datetime.datetime.now(), ' ', end='')
    print(arg)
    handle.cancel()  # 通过handle删除注册函数


def print_at(arg, loop):
    print(datetime.datetime.now(), ' ', end='')
    print(arg)
    loop.stop()

def stop_loop(loop):
    print(datetime.datetime.now(), ' timeout stop loop.')
    loop.stop()

def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    print(loop.time())

    handle = loop.call_at(loop.time() + 10, print_at, 'print_at.', loop)  # 在10s之后运行
    loop.call_soon(hello_world)  # 时间循环开始运行尽快调用hell_world.
    loop.call_later(5, print_delay, 'print_delay.', handle)  # 注册事件之后5s运行


    loop.call_at(loop.time()+20, stop_loop, loop)
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()

