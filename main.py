import socket
from time import sleep
from threading import Thread
from datetime import datetime

from funcs import do_work

SHUTDOWN = False


def main():
    global SHUTDOWN
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 5000))
        s.listen()
        while 1:
            sleep(0.0001)
            conn, addr = s.accept()
            request = conn.recv(4096)
            if not request:
                continue
            request = request.decode()
            if request == 'startup':
                SHUTDOWN = False
                conn.send('Started'.encode())
                conn.close()
                with open('log.txt', 'a') as file:
                    file.write(f'{datetime.now()}: STARTUP\n')
            elif SHUTDOWN:
                conn.send('Unavailable'.encode())
                conn.close()
            elif request == 'shutdown':
                SHUTDOWN = True
                conn.send('Shutdown'.encode())
                conn.close()
                with open('log.txt', 'a') as file:
                    file.write(f'{datetime.now()}: SHUTDOWN\n')
            elif request == 'ping':
                conn.send('pong'.encode())
                conn.close()
            else:
                thread = Thread(target=do_work, args=(conn,))
                thread.start()


if __name__ == '__main__':
    with open('log.txt', 'w') as file:
        file.write(f'{datetime.now()} START\n')
    main()
