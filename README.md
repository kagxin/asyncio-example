# asyncio-example

#### [helloworld.py](https://github.com/kagxin/asyncio-example/blob/master/helloworld.py)
> hello world
#### [calls.py](https://github.com/kagxin/asyncio-example/blob/master/calls.py)
> 在主事件中注册回调的例子
#### [parallel_hello_world.py](https://github.com/kagxin/asyncio-example/blob/master/parallel_hello_world.py)
> 使用协程执行并行任务的简单例子
#### [chain_coro.py](https://github.com/kagxin/asyncio-example/blob/master/chain_coro.py)
> 使用下载图片的例子说明链式协程的使用方式
#### [coro_functions.py](https://github.com/kagxin/asyncio-example/blob/master/coro_functions.py)
> asyncio.as_completed, asyncio.ensure_future, asyncio.wrap_future, asyncio.gather,COROUTINE asyncio.wait任务函数的使用的例子
#### [protocol_client.py](https://github.com/kagxin/asyncio-example/blob/master/protocol_client.py)
> asyncio协议的客户端代码例子
#### [protocol_server.py](https://github.com/kagxin/asyncio-example/blob/master/protocol_server.py)
> 带有心跳检测的，asyncio协议的服务端代码例子
#### [stream_client.py](https://github.com/kagxin/asyncio-example/blob/master/stream_client.py)
> asyncio stream 客户端例子
#### [stream_server.py](https://github.com/kagxin/asyncio-example/blob/master/stream_server.py)
> asyncio stream 服务端例子
#### [sync_primitive.py](https://github.com/kagxin/asyncio-example/blob/master/sync_primitive.py)
> 通过控制http请求的并发数量，说明Lock, Event, Condition, Semaphore 同步原语使用的例子
#### [aqueue.py](https://github.com/kagxin/asyncio-example/blob/master/aqueue.py)
> 用生产者消费者的模型来说明 asyncio.Queue 的使用方式
#### [consume_exception.py](https://github.com/kagxin/asyncio-example/blob/master/consume_exception.py)

>说明消费协程中异常的三种方式：
>1. 使用run_until_complete: 这个有局限，在协程内部不方便使用
>2. 在业务协程外包裹一个协程来消费这个异常 例如 例子中的： handle_exception
>3. 写一个装饰器，其实就是也就是使用的链式协程消费的异常只不过，协程了装饰器的形式，便于使用