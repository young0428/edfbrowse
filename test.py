<<<<<<< HEAD
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager,NamespaceProxy
import pyedflib
import time
class test1:
    def __init__(self,a):
        self._a = a
        self._b = 2
        self._run = True
    def get(self):
        return self._a
    @property
    def a(self):
        return self._a
    @property
    def b(self):
        return self._b

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self,value):
        self._run = value

    @a.setter
    def a(self,value):
        self._a = value

    @b.setter
    def b(self,value):
        self._b = value


class test1Proxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')
class edfProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')

def just_run(t1,edf):
    while t1.run:
        t1.a = t1.a+1
        print(t1.a)

    print(edf.readSignal(0,0,10))

class test2:
    def __init__(self,m):
        self.m = m
        self.inst = self.m.test1(10000)
        self.inst2 = self.m.EdfReader('C:/brainno05.edf')
        t = pyedflib.EdfReader('C:/brainno05.edf')
        print(type(t.readSignal(0,0,10)))
        p = Process(target=just_run,args=[self.inst,self.inst2])
        p.start()
        time.sleep(0.1)
        self.inst.run = False
        p.join()




if __name__ == '__main__':
    BaseManager.register('test1', test1,test1Proxy)
    BaseManager.register('EdfReader', pyedflib.EdfReader,edfProxy)
    
    manager = BaseManager()
    manager.start()
    test2(manager)
    #inst = manager.test1(10000)
    #t2 = test2(inst,)
    #inst2 = manager.EdfReader('C:/brainno05.edf')
   # p = Process(target=just_run,args=[inst,inst2])
   # p.start()
   # time.sleep(1)
   # inst.run = False
   # p.join()


=======
a = [1,2,3,4]
>>>>>>> ThreadDone
