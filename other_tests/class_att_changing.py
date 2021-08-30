class Test():
    def __init__(self, x):
        self.x = x
    
    def update_x(self, new_x):
        self.x = new_x
    
class Contain():
    def __init__(self):
        self.objects = []
    
    def add(self, items):
        for item in items:
            self.objects.append(item)

test_1 = Test('testing')
test_2 = Test('if')
test_3 = Test('this')
test_4 = Test('works')
container = Contain()
container.add([test_1, test_2, test_3, test_4])
print([obj.x for obj in container.objects])

test_1.update_x('this')
test_2.update_x('does')
test_3.update_x('work')
test_4.update_x('!')
print([obj.x for obj in container.objects])

del test_1
print([obj.x for obj in container.objects])
