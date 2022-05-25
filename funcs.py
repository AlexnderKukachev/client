import random
from asyncio import sleep
from datetime import datetime


# Функция задержки имитирующая работу сервиса
async def random_sleep():
    secs = random.uniform(0.1, 0.5)
    await sleep(secs)


def service_down():
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: SERVICE TURNED OFF\n')


def service_up():
    with open('log.txt', 'w') as file:
        file.write(f'{datetime.now()}: SERVICE TURNED ON\n')


def write_log(text: str, tip: int):
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {text}')
        file.write(f'{datetime.now()}: total tasks in progress - {tip}\n')
