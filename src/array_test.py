# b = [[0, 0, 0]] * 3
# b[0][1] = 1  # 这里因为初始[0,0,0]可以这样写数据，如果初始空数组则不能
# print(b)
# b[1].append(3)
# print(b)

# c = []
# c.append([1, 2, 3, 4])
# c.append([5, 6, 7, 8])
# c.append(9)
# print(c)

# b = [[] for i in range(4)]
# b[0] = 5
# b[1].append(6)
# b[1].append(7)
# print(b)
# print(len(b[1]))
# b[1].clear()
# print(b)
# b.append([1])

# a = [[[] for i in range(3)] for i in range(4)]
# print(a)

a = [[[] for i in range(24)] for i in range(6)]
# print(a)

a[5][1] = 1
# print(a)

a[5].clear()

print(a)
