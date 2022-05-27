import random
from time import sleep
from datetime import datetime

TASKS_IN_PROGRESS = 0


# Функция задержки имитирующая работу сервиса
def random_sleep():
    secs = random.uniform(0.1, 0.5)
    sleep(secs)


def do_work(conn):
    global TASKS_IN_PROGRESS
    TASKS_IN_PROGRESS += 1
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: total tasks in progress - {TASKS_IN_PROGRESS}\n')
    random_sleep()
    conn.send('Task_done'.encode())
    conn.close()
    TASKS_IN_PROGRESS -= 1
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: total tasks in progress - {TASKS_IN_PROGRESS}\n')


def write_log(text: str, tip: int):
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {text}')
        file.write(f'{datetime.now()}: total tasks in progress - {tip}\n')
