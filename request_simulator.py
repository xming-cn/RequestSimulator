import re
import time
import base64
import random
import asyncio
from enum import Enum, auto

from rich import console
console = console.Console()
print = console.print

import httpx
client = httpx.AsyncClient()


class SendPackageResult(Enum):
    TIMEOUT = auto()
    TRANSPORT_ERROR = auto()
    REQUEST_ERROR = auto()
    HTTP_ERROR = auto()
    UNKNOWN_ERROR = auto()

LOOKS_CORRECT_PARRERN = re.compile('ey[0-9A-Za-z]{230,280}')
def looks_correct(text: str):
    return re.fullmatch(LOOKS_CORRECT_PARRERN, text)

def response_correct(response: httpx.Response):
    if response.status_code != 200: return False
    if not looks_correct(response.text): return False
    return True

def random_token():
    plain_text = f'ICanHazUnicorn4-ws-ec2?-{random.randint(1, 10000)}'
    sample_string_bytes = plain_text.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

async def send_package(url: str, method: str, timeout: int=8):
    method = method.lower()
    method_callable = getattr(client, method)
    try:
        return await method_callable(url, timeout=timeout)
    except httpx.TimeoutException:
        return SendPackageResult.TIMEOUT
    except httpx.TransportError:
        return SendPackageResult.TRANSPORT_ERROR
    except httpx.RequestError:
        return SendPackageResult.REQUEST_ERROR
    except httpx.HTTPError:
        return SendPackageResult.HTTP_ERROR
    except Exception:
        return SendPackageResult.UNKNOWN_ERROR


def generate_calc_url(base_url: str):
    suffix = f'calc?input={random_token()}'
    return base_url + ('' if base_url.endswith('/') else '/') + suffix, '/' + suffix

HIDE_START = True
async def send_calc_package(url: str, method: str, timeout: int=8):
    calc_url, suffix = generate_calc_url(url)
    if not HIDE_START: print(f'[dark_gray]start send to {calc_url}[/dark_gray]')
    start = time.time()
    response = await send_package(calc_url, method, timeout)
    spend_time = round((time.time() - start) * 100) / 100
    if isinstance(response, SendPackageResult):
        print(f'[red]  {response} in {spend_time:>5.2f}s[/red] [yellow]{suffix}[/yellow]')
    elif response_correct(response):
        print(f'[green]  CORRECT in {spend_time:>5.2f}s[/green] [yellow]{suffix}[/yellow] [gray]{response.text[:20]}....[/gray]')
    elif hasattr(response, "reason"):
        print(f'[red]INCORRECT in {spend_time:>5.2f}s[/red] [yellow]{suffix}[/yellow] [gray]{response.status_code} {response.reason}[/gray]')
    elif hasattr(response, "text"):
        print(f'[red]INCORRECT in {spend_time:>5.2f}s[/red] [yellow]{suffix}[/yellow] [gray]{response.status_code} {response.text}[/gray]')
    else:
        print(f'[red]INCORRECT in {spend_time:>5.2f}s[/red] [yellow]{suffix}[/yellow] [gray]{response.status_code}[/gray]')

async def main(times: int, package_pre_times: int, interval: int, url: str, method: str, timeout: int=8):
    all_tasks = []
    while times != 0:
        for _ in range(package_pre_times):
            task = asyncio.create_task(send_calc_package(url, method, timeout))
            all_tasks.append(task)
        await asyncio.sleep(interval)
        times -= 1
    await asyncio.gather(*all_tasks)

url = 'http://gameday-lb-171313428.us-east-2.elb.amazonaws.com'
method = 'get'
timeout = 8

times = -1
package_pre_times = 1
interval = 2

if __name__ == '__main__':
    asyncio.run(main(times, package_pre_times, interval, url, method, timeout))
