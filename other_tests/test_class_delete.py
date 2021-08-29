class Obj():
    def __init__(self, x):
        self.x = x

class Contain():
    def __init__(self):
        self.objs = []
    
    def add_obj(self, obj):
        self.objs.append(obj)

obj = Obj(1)
objs = [obj, Obj(2), Obj(3)]
test = Contain()
test.add_obj(obj)

del obj
print(test)
print(len(objs))
print(obj)
print(test.objs)