# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager

def get_task_queue(addr=('127.0.0.1', 6000), authkey=b'kk'):
    class QueueManager(BaseManager):
        pass

    manager = QueueManager(address=addr, authkey=authkey)
    manager.register('get_task_queue')
    manager.connect()

    t_q = manager.get_task_queue()
    return t_q

def get_task(t_q):
    task = t_q.get()
    return task

if __name__ == '__main__':
    t_q = get_task_queue()
    print(get_task(t_q))