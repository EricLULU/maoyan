import aiohttp
import asyncio
import re
import time


#获取函数
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def run(url):
    async with aiohttp.ClientSession() as session:
        return await fetch(session, url)


def url_cre():
    url_start = "http://maoyan.com/board/4?offset="
    for i in range(10):
        url = url_start + str(i*10)
        yield url
async def info_get(html):
    p2 = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?class="name".*?><a.*?>(.*?)</a>.*?"star".*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(p2,html)
    for item in items:
        info = {
                    'index':item[0],
                    'title':item[1],
                    'actor':item[2].strip().split('：')[-1],
                    'time':item[3].split('：')[-1],
                    'score':item[4]+item[5],
                }
        print(info)
        #self.save_to_csv(info)

async def main():
    for url in url_cre():
        #url = await url_cre()
        html = await run(url)   #获取url
        await info_get(html)
        #print(len(html))
s_time = time.time()  
loop = asyncio.get_event_loop()   #获时间循环
loop.run_until_complete(main())
e_time = time.time()
print("总耗时:", e_time-s_time)