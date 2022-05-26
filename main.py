from aiohttp import web
from funcs import random_sleep, service_down, service_up
from datetime import datetime
import atexit

app = web.Application()
routes = web.RouteTableDef()

shutdown = True
url = '/api'


# Проверка доступен ли сервис
@routes.get(f'{url}/is_alive/')
async def status(request):
    if shutdown:
        return web.json_response(not shutdown, status=503)
    else:
        return web.json_response(not shutdown, status=200)


# Маршрут для отправки задачи
@routes.get('/api/task/{num}')
async def work_task(request):
    task = f'task_{request.match_info["num"]}'
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - in progress\n')
    await random_sleep()
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - done\n')
    return web.json_response(text=task, status=200)


# Маршрут для отправки задачи
@routes.post('/api/task/{num}')
async def work_task(request):
    task = f'task_{request.match_info["num"]}'
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - in progress\n')
    await random_sleep()
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - done\n')
    return web.json_response(text=task, status=200)


# Маршрут для отправки задачи
@routes.put('/api/task/{num}')
async def work_task(request):
    task = f'task_{request.match_info["num"]}'
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - in progress\n')
    await random_sleep()
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - done\n')
    return web.json_response(text=task, status=200)


# Маршрут для отправки задачи
@routes.delete('/api/task/{num}')
async def work_task(request):
    task = f'task_{request.match_info["num"]}'
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - in progress\n')
    await random_sleep()
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - done\n')
    return web.json_response(text=task, status=200)


# Маршрут для отправки задачи
@routes.patch('/api/task/{num}')
async def work_task(request):
    task = f'task_{request.match_info["num"]}'
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - in progress\n')
    await random_sleep()
    if shutdown:
        return web.json_response(text=task, status=503)
    with open('log.txt', 'a') as file:
        file.write(f'{datetime.now()}: {task} - done\n')
    return web.json_response(text=task, status=200)


# Команда запуск сервиса
@routes.get(f'{url}/start/')
async def start(request):
    global shutdown
    if shutdown:
        with open('log.txt', 'a') as file:
            file.write(f'{datetime.now()}: SERVICE STARTUP\n')
    shutdown = False
    return web.Response(text='Started', status=200)


# Команда остановки сервиса
@routes.get(f'{url}/stop/')
async def stop(request):
    global shutdown
    if not shutdown:
        with open('log.txt', 'a') as file:
            file.write(f'{datetime.now()}: SERVICE SHUTDOWN\n')
    shutdown = True
    return web.Response(text='Stopped', status=200)


app.add_routes(routes)

if __name__ == '__main__':
    service_up()
    atexit.register(service_down)
    web.run_app(app, host='0.0.0.0', port=5000)
