# ！/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from multiprocessing import Queue

class ManagerServer(object):
    '''用于分布式进程的创建和连接。
       服务端可以直接运行本模块，或者：
       >>> from manager_server import ManagerServer
       >>> server = ManagerServer()
       >>> server.start_server()
       运行端：
       >>> from manager_server import ManagerServer
       >>> server = ManagerServer()
       >>> server.connect_server()
       >>> queue_task, queue_resault = server.get_queue()
    '''

    def __init__(self, addr=('127.0.0.1',6000), authkey=b''):
        class MyManager(BaseManager):
            pass
        self.manager = MyManager(address=addr, authkey=authkey)

    def start_server(self):
        '''用于服务端,开始监听端口。'''
        q_t = Queue()
        q_r = Queue()
        self.manager.register('get_task_queue', callable=lambda:q_t)
        self.manager.register('get_resault_queue', callable=lambda:q_r)
        print('服务运行在 %s:%s' % self.manager.address)
        s = self.manager.get_server()
        s.serve_forever()

    def connect_server(self):
        '''用于任务进程，连接服务器。'''
        self.manager.register('get_task_queue')
        self.manager.register('get_resault_queue')
        self.manager.connect()

    def get_queue(self):
        '''用于任务进程，获取队列。
           默认获取任务列队:get_task_queue
           默认获取结果列队:get_resault_queue
           并以元组的形式返回任务列队和结果列队。'''
        q_t = self.manager.get_task_queue()
        q_r = self.manager.get_resault_queue()
        return q_t, q_r

if __name__ == '__main__':
    from threading import Thread
    import time
    server = ManagerServer()
    def begin(server):
        server.start_server()

    def stop(server):
        while True:
            temp = input('type "q" to close!')
            if temp.lower() == 'q':
                break
            else:
                continue
    t1 = Thread(target=begin, args=(server,))
    t1.start()
    time.sleep(1)
    t2 = Thread(target=stop, args=(server,))
    t2.start()
    t2.join()
    print('连接关闭！')
    time.sleep(2)