# ！/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from multiprocessing import Queue

class ManagerServer(object):
    '''用于分布式进程的创建和连接。
    '''

    def __init__(self, addr=('127.0.0.1',6000), authkey=b'', **kwargs):
        class MyManager(BaseManager):
            pass
        self.manager = MyManager(address=addr, authkey=authkey)
        self.kwargs = kwargs

    def start_server(self):
        '''用于服务端,开始监听端口。'''
        q_t = Queue()
        q_r = Queue()
        self.manager.register('get_task_queue', callable=lambda:q_t)
        self.manager.register('get_resault_queue', callable=lambda:q_r)
        if self.kwargs:
            for k,v in self.kwargs.items():
                exec('%s = Queue()' % k)
                self.manager.register(v, exec('callable=lambda:%s' % k))
        s = self.manager.get_server()
        print('服务运行在 %s:%s' % self.manager.address)
        s.serve_forever()

    def close_server(self):
        '''用于关闭连接。'''

        self.manager.shutdown()

    def connect_server(self):
        '''用于任务进程，连接服务器。'''
        self.manager.register('get_task_queue')
        self.manager.register('get_resault_queue')
        if self.kwargs:
            for v in self.kwargs.values():
                self.manager.register(v)
        self.manager.connect()

    def get_queue(self, exe):
        '''用于任务进程，获取队列。
           默认获取任务列队:get_task_queue
           默认获取结果列队:get_resault_queue'''
        exe = 'self.manager.%s()' % exe
        q = exec(exe)
        return q

if __name__ == '__main__':
    server = ManagerServer()
    server.start_server()
    