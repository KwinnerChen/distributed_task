# !usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from multiprocessing import Queue
import threading
import re

def main(addr=('',6000), authkey=b'kk'):

    class MyManager(BaseManager):
        pass

    q_t = Queue()
    q_r = Queue()

    manager = MyManager(address=addr, authkey=authkey)

    manager.register('get_task_queue', callable=lambda:q_t)
    manager.register('get_resault_queue', callable=lambda:q_r)
    server = manager.get_server()

    def start_server(server):
        print('队列服务器正在运行......')
        server.serve_forever()

    def stop_server(server):
        temp = input('输入q关闭服务器。')
        if temp == 'q':
            try:
                assert server.shutdown(server)
            except AssertionError:
                return

    t1 = threading.Thread(target=start_server, args=(server,))
    t1.start()
    t2 = threading.Thread(target=stop_server, args=(server,))
    t2.start()
    t1.join()
    print('服务器已关闭！')   

if __name__ == '__main__':
    temp = input('是否以默认配置运行服务器（address=('',6000), authkey=None)?Y/N')
    if temp.lower() == 'y':
        main()
    elif temp.lower() == 'n':
        while True:
            addr = input('自定义服务器地址：')
            try:
                assert re.match(r'\b((25[1-5]|2[0-4]\d|1\d\d|\d?\d)\.){3}:\d+\b', addr)
                break
            except AssertionError:
                print('请检查服务器地址是否为IP格式(1.2.3.4:5。')
                continue
        ip = addr.split(':')[0]
        port = int(addr.split(':')[-1])
        addr = (ip, port)
        authkey = input('输入连接密钥：')
        main(addr=addr, authkey=authkey)
    