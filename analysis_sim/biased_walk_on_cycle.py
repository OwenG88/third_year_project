import random
import matplotlib.pyplot as plt
import numpy as np

n = 30
k = 3
bound = int(30 * (2 * (k -1) / k)**n)

pos = int(np.random.binomial(n, 0.5))
poss = []
jackpot = 0
counter = 0
for i in range(bound): 
    counter += 1
    pos = int(np.random.binomial(n, 0.5))
    for j in range(3 * n):
        print(pos)
        if pos == 0 or pos == n:
            print(counter)
            exit()
        elif random.random() <= 1/ k:
            pos -= 1
        else:
            pos += 1

        

        # poss.append(pos) 
    
# x = [i for i in range(3 * n * bound)]
# if jackpot > 0:
#     print("All is good")
#     print(jackpot, bound)
# else:
#     print("BADDD")
#     print(jackpot, bound)
# plt.scatter(x, poss)
# plt.show()
    
# print(counter)