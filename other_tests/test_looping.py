test = [1,2,3,4,5]

for t in test:
    print(t)
    if t == 1:
        test.remove(4)
        print(test)
    if t == 3:
        test.remove(1)
        print(test)

print(test)