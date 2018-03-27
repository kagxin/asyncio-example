import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.DEBUG)

async def slow_operation(op_name, future, n):
    await asyncio.sleep(n)
    future.set_result(op_name)


async def slow_operation2(op_name, n):
    await asyncio.sleep(n)
    return op_name


def main1():
    """
    ensure_future:
        将协程封装为task，加入时间循环进行调度
    """
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    future = asyncio.Future()
    asyncio.ensure_future(slow_operation('op1', future, 2))

    try:
        loop.run_until_complete(future)
    except Exception as e:
        print(str(e))
    else:
        print(future.result())
    finally:
        loop.stop()
        loop.close()


def main2():
    """
    as_completed :
    :return: 
    """
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    # async def as_completed_ex():
    #     future1 = asyncio.Future()
    #     future2 = asyncio.Future()
    #     future3 = asyncio.Future()
    #     asyncio.ensure_future(slow_operation('op1', future1, 1))
    #     asyncio.ensure_future(slow_operation('op2', future2, 2))
    #     asyncio.ensure_future(slow_operation('op3', future3, 3))
    #     for f in asyncio.as_completed([future1, future3, future2]):  #等待future完成，返回最先完成的
    #         res = await f
    #         print(res)
    # try:
    #     loop.run_until_complete(as_completed_ex())
    # finally:
    #     loop.stop()
    #     loop.close()

    future1 = asyncio.Future()
    future2 = asyncio.Future()
    future3 = asyncio.Future()
    asyncio.ensure_future(slow_operation('op1', future1, 1))
    asyncio.ensure_future(slow_operation('op2', future2, 2))
    asyncio.ensure_future(slow_operation('op3', future3, 3))
    for f in asyncio.as_completed([future1, future3, future2]):  #最先完成的future会迭代出来
        try:
            res = loop.run_until_complete(f)
            print(res)
        except Exception as e:
            print(e)

    loop.stop()
    loop.close()


def main3():
    """
    gather
    :return: 
    """
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    gather = asyncio.gather(
        slow_operation2('op1', 1),
        slow_operation2('op3', 3),
        slow_operation2('op2', 2)
    )

    try:
        sl = loop.run_until_complete(gather)
        print(sl)
    finally:
        loop.stop()
        loop.close()

def main4():
    """
    wait
    :return: 
    """
    get_result = lambda f: f.result()

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    w = asyncio.wait((
        slow_operation2('op1', 1),
        slow_operation2('op3', 3),
        slow_operation2('op2', 2)
    ), timeout=2)  # 2s 之后超时

    try:
        done, pending = loop.run_until_complete(w)  #等待执行结束或超时, 2s超时
        print(list(map(get_result, done)), pending)  # 拿到完成的fs，和pending的fs

        pw = asyncio.wait(pending)
        done, pending = loop.run_until_complete(pw)  # 等待pending的fs直到完成
        print(list(map(get_result, done)), pending)
    finally:
        loop.stop()
        loop.close()

def main5():
    """
    wrap_future
    :return:
    """
    def slow_operation3(op_name, n):
        import time
        time.sleep(n)
        # if op_name == 'op2':
        #     raise ValueError('test')
        return op_name

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    executor = ThreadPoolExecutor(max_workers=2)
    c_futures = [executor.submit(slow_operation3, op, i) for i, op in enumerate(('op1', 'op2'))]  # 提交操作函数，拿到其对应的两个futures
    a_futures = map(asyncio.wrap_future, c_futures)  # 使用asyncio.wrap_future, 把concurrent.future 的future封装成协程的future
    gs = asyncio.gather(*a_futures)  # 使用gather，拿到多个协程的aggregating 形态
    try:
        rs = loop.run_until_complete(gs)  # 等待协程任务完成
        print(rs)
    finally:
        loop.stop()
        loop.close()



if __name__ == '__main__':
    main5()