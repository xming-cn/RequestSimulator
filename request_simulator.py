import re
import time
import httpx
import random
import asyncio

from rich import console
console = console.Console()
print = console.print

client = httpx.AsyncClient()

LOOKS_CORRECT_PARRERN = re.compile('ey[0-9A-Za-z]{230,280}')
def looks_correct(text: str):
    return re.fullmatch(LOOKS_CORRECT_PARRERN, text)

def response_correct(response: httpx.Response):
    if response.status_code != 200: return False
    if not looks_correct(response.text): return False
    return True

def random_token():
    return str(random.randint(1000000, 9999999))

async def send_package(url: str, method: str, timeout: int=8):
    method = method.lower()
    method_callable = getattr(client, method)
    try:
        return await method_callable(url, timeout=timeout)
    except httpx.ReadTimeout:
        return None

def generate_calc_url(base_url: str):
    return base_url + '/calc?' + random_token()

async def send_calc_package(url: str, method: str, timeout: int=8):
    calc_url = generate_calc_url(url)
    print(f'[dark_gray]start send to {calc_url}[/dark_gray]')
    start = time.time()
    response = await send_package(calc_url, method, timeout)
    spend_time = round((time.time() - start) * 100) / 100
    if response is None:
        print(f'[red]  TIMEOUT in {spend_time}s[/red] [yellow]{calc_url}[/yellow]')
    elif response_correct(response):
        print(f'[green]  CORRECT in {spend_time}s[/green] [yellow]{calc_url}[/yellow] [gray]{response.text[:20]}....[/gray]')
    elif hasattr(response, "reason"):
        print(f'[red]INCORRECT in {spend_time}s[/red] [yellow]{calc_url}[/yellow] [gray]{response.status_code} {response.reason}[/gray]')
    else:
        print(f'[red]INCORRECT in {spend_time}s[/red] [yellow]{calc_url}[/yellow] [gray]{response.status_code}[/gray]')

async def main(times: int, package_pre_times: int, interval: int, url: str, method: str, timeout: int=8):
    all_tasks = []
    while times != 0:
        for _ in range(package_pre_times):
            task = asyncio.create_task(send_calc_package(url, method, timeout))
            all_tasks.append(task)
        await asyncio.sleep(interval)
        times -= 1
    await asyncio.gather(*all_tasks)


url = 'http://18.191.202.35'
method = 'post'
timeout = 10

times = 20
package_pre_times = 2
interval = 1

asyncio.run(main(times, package_pre_times, interval, url, method, timeout))