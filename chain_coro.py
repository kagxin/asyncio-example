import asyncio
import aiohttp
from functools import partial
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.DEBUG)

SRCS = ['http://cdn.daweijita.com/2016/06/tab_weiwenhuaming_secret-base_tanchang_1.gif',
        'http://cdn.daweijita.com/2016/06/tab_weiwenhuaming_secret-base_tanchang_2.gif',
        'http://cdn.daweijita.com/2016/06/tab_weiwenhuaming_secret-base_tanchang_3.gif',
        'http://cdn.daweijita.com/2016/06/tab_weiwenhuaming_secret-base_tanchang_4.gif',
        'http://cdn.daweijita.com/2016/06/tab_weiwenhuaming_secret-base_tanchang_5.gif',
        'http://cdn.daweijita.com/2016/06/tab_weiwenhuaming_secret-base_tanchang_6.gif'
    ]


def save_image():  # 用一个闭包做文件名的区分，没吊用一次加一
    count = 0
    def save(image):
        nonlocal count
        path = './'+str(count)+'.gif'
        count += 1
        with open(path, 'wb') as fp:
            fp.write(image)
    return save


async def get_image(url):  # 下载图片
    session = aiohttp.ClientSession()
    resp = await session.get(url)
    image = await resp.read()
    session.close()
    return image


async def download_one(url, save):  # 下载并保存一个图片, 链式协程
    image = await get_image(url)
    save(image)


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    si = save_image()  # 拿到闭包
    wait = asyncio.wait(map(partial(download_one, save=si), SRCS))  # 获取所有的src， 这里map函数得到一个获取各个图片的协程集合，一个可迭代对象
    # gather = asyncio.gather(*map(partial(download_one, save=si), SRCS))

    try:
        loop.run_until_complete(wait)  #
    finally:
        loop.close()
        loop.stop()


if __name__ == '__main__':
    main()

