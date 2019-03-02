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
        http_rq = await ioloop.run_in_executor(executor,
                                               partial(request.urlopen, url))
        print(f'Done  - {url}')
        return url, len(http_rq.read()), running_time(), http_rq.getcode()
    except error.HTTPError as e:
        print(f'Error - {url}')
        return url, 0, running_time(), e


template = 'http://www.{}.com'
executor = Executor(len(urls))
ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(fetch(template.format(url), ioloop, executor))
         for url in urls]

start_time = time()
ioloop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    url, size, seconds, code = task.result()
    print(f'{url} {bytes_to_human(size)} {seconds_to_human(seconds)} '
          f'{code}')

    if task.exception():
        print(f'Exception on {task.exception()}')

ioloop.close()
