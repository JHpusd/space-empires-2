
class Test:
    def __init__(self):
        self.asdf = {}
    
    def update_asdf(self, new_asdf):
        self.asdf = new_asdf


test = [(1,1), (1,2), (2,3), (1,3), (2,3), (2,5)]

for item in test:
    if item[0] == 1:
        test.remove(item)
        print(test)
print([item for item in test if item[0] != 1])