# coding: utf-8
import random
if __name__ == '__main__':
    x = [random.randint(10, 10000) for _ in range(10)]
    x_copy = x.copy()
    print(x)
    max_len = len(str(max(x)))
    for i, num in enumerate(x):
        x[i] = (max_len - len(str(num))) * '0' + str(num)

    for i in range(max_len)[::-1]:
        res = []
        for j in range(10):
            for num in x:
                if num[i] == str(j):
                    res.append(num)
        x = res
        print(i, ":", x)

    x = [int(_) for _ in x]
    print(x)

    x_copy.sort()

    if not (x == x_copy):
        print(1, x_copy)
