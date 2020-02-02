import multiprocessing
import time
from multiprocessing.managers import BaseManager

class MyManager(BaseManager): pass


def Manager():
    m = MyManager()
    m.start()
    return m 

class Myclass():
    def __init__(self):
        self._value = 3
    def update(self,value):
        self._value += value

    def p(self,main=None):
        print('called from main')
        print(self._value)

def use(mclass,i):
    
    for j in range(1,101):
        mclass.update(j)
        print('process %d'%i,'add %d'%j)
        mclass.p()
      


    print('------------precess %d done-----------'%i)




    return mclass



MyManager.register('Myclass', Myclass)
def main():
    manager = Manager()
    myclass =manager.Myclass()
    print(myclass)

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    start = time.time()
    for i in range(10):
        pool.apply_async(func = use,args=(myclass,i))

    print('---here is main---')
    myclass.p('nono')
    print('-------------')
    pool.close()
    pool.join()

    print(multiprocessing.cpu_count())
    print(time.time()-start)

if __name__=='__main__':
    main()



