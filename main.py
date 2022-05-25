from aiohttp import web
from funcs import random_sleep, service_down, service_up, write_log
from datetime import datetime
import atexit

app = web.Application()
routes = web.RouteTableDef()

shutdown = True
url = '/api'
tasks_in_progress = 0


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
    global tasks_in_progress
    task = f'task_{request.match_info["num"]}'
    if shutdown:
        write_log(f'{task} - aborted\n', tasks_in_progress)
        return web.Response(text=task, status=503)
    tasks_in_progress += 1
    write_log(f'{task} - in progress\n', tasks_in_progress)
    await random_sleep()
    tasks_in_progress -= 1
    if shutdown:
        write_log(f'{task} - aborted\n', tasks_in_progress)
        return web.Response(text=task, status=503)
    write_log(f'{task} - done\n', tasks_in_progress)
    return web.Response(text=task, status=200)


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
