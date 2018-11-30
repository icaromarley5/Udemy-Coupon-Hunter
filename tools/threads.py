# -*- coding: utf-8 -*-

import  threading

original_active_threads = threading.activeCount()

def allFinalized():
    return numberAtives() == 0

def numberAtives():
    global original_active_threads
    return threading.activeCount() - original_active_threads


class TaskThread(threading.Thread):

    def __init__(self,func,args):
        threading.Thread.__init__(self)
        self.kwargs = args
        self.func = func
        self.result = ""

    def run (self):
        try:
            self.result = self.func(**self.kwargs)#desempacotamento
        except Exception as e:
            print("Exceção ({}) na função {} com os argumentos {}".format(str(e),self.func,self.kwargs))
                  
    def join(self):
        threading.Thread.join(self)
        return self.result