import asyncio
import aiohttp


@asyncio.coroutine
def func1():
    print("hello world from func1")
    yield from asyncio.sleep(1)
    print("hello world again from func1")


# 等价版本
async def func2():
    print('hello world from func2')
    await asyncio.sleep(1)
    print("hello world again from func2")


async def req(url):
    # 这个地方可以设置headers和timeout
    async with aiohttp.ClientSession() as session:
        # url = 'http://ww3.sinaimg.cn/mw600/0073tLPGgy1fwuioob59zj30np0zkagu.jpg'
        # 这个地方可以设置proxy
        resp = await session.get(url)
        image = await resp.read()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, save, image, url)


def save(image, url):
    with open(url.split('/')[-1], 'wb') as file:
        file.write(image)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(list(req(url) for url in ['http://ww3.sinaimg.cn/mw600/0073tLPGgy1fwuioob59zj30np0zkagu.jpg', 'http://ww3.sinaimg.cn/mw600/006XNEY7gy1fwuioi1aynj30np0zkafv.jpg', 'http://ww3.sinaimg.cn/mw600/0073tLPGgy1fwuiobsfpdj30np0zkn39.jpg'])))
