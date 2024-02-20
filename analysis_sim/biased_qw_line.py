import numpy as np 
import random 
import matplotlib.pyplot as plt
import math

n = 1000
k = 3
# n_steps = 7
rho = 1 / k


position_state = [math.comb(n, i) / 2 ** n for i in range(n+1)] 
coin_state = [1/np.sqrt(2), 1/np.sqrt(2)]
inital_state = np.kron(position_state, coin_state)
#This is going 1L, 1R, 2L, 2R, ...
shift_operator = np.zeros((2*(n+1), 2*(n+1)))


for i in range(2):
    for j in range(n+1):
        a = np.zeros(2*(n+1))
        b= np.zeros(2*(n+1))
        a[2*j + i] = 1
        if 0 <=j + (-1)**i <= n:
            b[2*j + i + 2*(-1)**i] = 1
        partial = np.outer(b, a.conj().T)
        shift_operator += partial


coin_operator = [[np.sqrt(rho), np.sqrt(1-rho)], [np.sqrt(1-rho), -np.sqrt(rho)]]

evolution_operator = shift_operator @ np.kron(np.eye(n+1), coin_operator)
final_state = inital_state

probs = []
bound = 20000
for n_steps in range(1, bound):
    final_state = evolution_operator @ final_state

    ##Get the probability we are at 0
    normalise = np.linalg.norm(final_state)

    states = final_state / normalise
    prob = np.abs(states)**2
    # print(prob)

    ## For n = 100
    # if 255 < n_steps < 285:
    #     print(n_steps, prob[1])
    probs.append(prob[1])


x = np.arange(1, bound)

print(n, np.argmax(probs)+1) 
plt.plot(x, probs)
plt.show()

# print(prob[n])
# print(prob)
# print(normalise)
# prob = np.abs((final_state[0] + final_state[n + 1]) / normalise)**2
# print(prob)
