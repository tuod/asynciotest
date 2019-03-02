import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor
from urllib import request, error
from functools import partial
from time import time, sleep


urls = """google twitter facebook youtube pinterest tumblr
instagram reddit flickr meetup classmates microsoft apple
linkedin xing renren disqus snapchat twoo whatsapp""".split()


def bytes_to_human(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f} {x}'
        num /= 1024.0


def seconds_to_human(sec):
    for x, y in [(60, 'seconds'), (60, 'minutes'), (24, 'hours'),
                 (7, 'days'), (0, 'weeks')]:
        if sec < x or not x:
            return f'{sec:.1f} {y}'
        sec /= x


def running_time():
    return time() - start_time


async def fetch(url, ioloop, executor):
    try:
        # print(f'{url} - start task')
        http_rq = await ioloop.run_in_executor(executor, partial(request.urlopen, url))
        data = http_rq.read
        code = http_rq.getcode
        # sleep(3)
        print(f'{url} - code {code()} - {bytes_to_human(len(data()))} - {seconds_to_human(running_time())}')
    except error.HTTPError as e:
        print(f'{url} - Exception {e} - {running_time():.2f} sec')


template = 'http://www.{}.com'
executor = Executor(len(urls))
ioloop = asyncio.get_event_loop()
# ioloop.set_debug(True)
tasks = [ioloop.create_task(fetch(template.format(url), ioloop, executor)) for url in urls]

start_time = time()
ioloop.run_until_complete(asyncio.wait(tasks))

ioloop.close()
