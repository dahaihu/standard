import asyncio


@asyncio.coroutine
def func():
    print("hello world")
    yield from asyncio.sleep(1)
    print("hello world again")


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([func(), func()]))
