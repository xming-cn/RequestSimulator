import csv
import time
import asyncio
import request_simulator
from rich.progress import track

from rich import console
console = console.Console()
print = console.print

url = 'http://web-lb-1888488606.us-east-2.elb.amazonaws.com'
method = 'get'
timeout = 30

with open('requests.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    next(spamreader)
    
    for i, row in enumerate(spamreader):
        times, package_pre_times, interval = row
        times = int(times)
        package_pre_times = int(package_pre_times)
        interval = float(interval)
        if package_pre_times > 0:
            print(f'[cyan]▶ 开始运行阶段 {i+1}[/cyan] [gray]在接下来 {interval * times} 秒内, 每 {interval} 秒将发送 {package_pre_times} 次请求[/gray]')
            asyncio.run(request_simulator.main(
                times, package_pre_times, interval, url, method, timeout
            ))
        else:
            sleep_time = int(interval * times)
            print(f'[cyan]▶ 开始运行阶段 {i+1}:[/cyan] [gray]休息 {sleep_time} 秒![/gray]')
            for i in track(range(sleep_time), description="休息中..."):
                time.sleep(1)