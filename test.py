import sys

class test:
    def __init__(self):
        self.a = []


a = test()
a.a.append(1)
print(sys.getsizeof(a))
a.a.append(2)
print(sys.getsizeof(a))
for i in range(100):
    a.a.append(i)

print(sys.getsizeof(a))
print(a.a)