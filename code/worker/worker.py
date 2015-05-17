import asyncio

@asyncio.coroutine
def watermark():
    print('Watermark image')
    yield from asyncio.sleep(3)

@asyncio.coroutine
def worker():
    # Setup connection to Cloud Queues
    while True:
        print('Check queue for work')
        yield from watermark()

def event_loop():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker())
    finally:
        loop.close()

if __name__ == '__main__':
    event_loop()