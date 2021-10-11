
class Test:
    def __init__(self):
        self.asdf = {}
    
    def update_asdf(self, new_asdf):
        self.asdf = new_asdf

t = Test()
print(t.asdf)
t.update_asdf({'1': 1, '2': 2})
print(t.asdf)