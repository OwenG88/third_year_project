##Biased walk on the line
##We move left with probability 1/k
##and right with probability 1 - 1/k
##Implementation of Eppstein's analysis
##of Schöning's algorithm

import random
import matplotlib.pyplot as plt
import numpy as np

n = 50
k = 3
# bound = int(30 * (2 * (k -1) / k)**n)
bound = int((2 * (k -1) / k)**n)
print(bound)

pos = int(np.random.binomial(n, 0.5))
poss = []
jackpot = 0
for i in range(bound): 
    pos = int(np.random.binomial(n, 0.5))
    for j in range(3 * n):
        if pos == 0:
            jackpot += 1 
            pos += 1
        elif pos == n:
            pos -= 1
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
    
print(jackpot, bound)