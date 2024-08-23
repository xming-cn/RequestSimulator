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

with open('varying_rule.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    varying_rule = list(spamreader)[1:]

for i, row in enumerate(varying_rule):
    duration, interval, package_pre_times = int(row[0]), float(row[1]), int(row[2])

    if package_pre_times > 0:
        times = duration // interval
        duration = times * interval
        print()
        print(f'[cyan]▶ 开始运行阶段 {i+1}[/cyan]')
        print(f'[gray]  在接下来 {duration} 秒内, 每 {interval} 秒将发送 {package_pre_times} 次请求[/gray]')
        print()
        asyncio.run(request_simulator.main(
            times, package_pre_times, interval, url, method, timeout
        ))
    else:
        print()
        print(f'[cyan]▶ 开始运行阶段 {i+1}:[/cyan] [gray]休息 {duration} 秒![/gray]')
        for i in track(range(duration), description="休息中..."):
            time.sleep(1)
        print()