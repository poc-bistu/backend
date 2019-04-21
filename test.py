list = [True, True, True, True]
for i in range(8):
    for i in range(4):
        if list[i] == True:
            list[i] = False
            break
    print(list)