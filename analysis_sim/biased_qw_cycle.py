import numpy as np 
import random 
import matplotlib.pyplot as plt
import math

n = 100
k = 2
# n_steps = 7
rho = 1 / k #probability of going left

def make_y(prob):
    y = []
    c = 0
    for i in range(len(prob)):
        if i % 2 == 0:
            c += 1
            e = prob[i] + prob[i + 1]

            y.append(e)
    return y

position_state = [math.comb(n, i) / 2 ** n for i in range(n)]
position_state[0] += 1 / 2 ** n 

coin_state = [np.sqrt(rho), np.sqrt(1 - rho)]
inital_state = np.kron(position_state, coin_state)
# print(len(inital_state))
#This is going 1L, 1R, 2L, 2R, ...
shift_operator = np.zeros((2*n, 2*n))


x = []
for i in range(2):
    coin = (1 - i)
    for j in range(n):
        a = np.zeros(2*n)
        b = np.zeros(2*n)
        a[2*j + coin] = 1
        # x += [2*j + i]

        # # if 0 <=j + (-1)**i <= n:
     
        # if (i == 0 and j == n):
        #     print(i,j)
        #     b[1] = 1
        # else:
        #     # print(i,j)
        b[(2*j + coin + 2*(-1)**i) % (2*n)] = 1

        # if (i == 1 and j == 0):
        #     print("here")
        #     b[2*j + i - 1] = 0
        # elif (i == 0 and j == n - 1):
        #     print("here1")
        #     b[2*j + i + 1] = 0
        # else:
        #     b[2*j + i + 2*(-1)**i] = 1
        # partial = np.outer(b, a.conj().T)
        # # partial = np.outer(b, a)
        # shift_operator += partial
        shift_operator[2*j + coin][(2*j + coin + 2*(-1)**i) % (2*n)] = 1

S = np.matrix(shift_operator)
# print(S)
# print(x)
S2 = S.copy() 
myI = S @ S2.conj().T
# print(myI)
assert np.array_equal(myI, np.eye(2*n))


coin_operator = [[np.sqrt(rho), np.sqrt(1-rho)], [np.sqrt(1-rho), -np.sqrt(rho)]]

evolution_operator = shift_operator @ np.kron(np.eye(n), coin_operator)
final_state = inital_state

probs = []
bound = 500
ys=  []
for n_steps in range(bound):
    final_state = evolution_operator @ final_state

    ##Get the probability we are at 0
    normalise = np.linalg.norm(final_state)

    states = final_state / normalise
    prob = np.abs(states)**2
    # print(prob)

    if n_steps % 100 == 0: 
        ys += [make_y(prob)]

    ## For n = 100
    # if 255 < n_steps < 285:
    #     print(n_steps, prob[1])
    probs.append(prob[0] + prob[1])



y = make_y(prob)

x = np.arange(0, bound)
x2 = np.arange(0, n)

print(n, np.argmax(probs)+1) 


plt.title("Probability Distribution of a Biased Quantum-Walk on the Cycle")
plt.xlabel("Number of steps")
plt.ylabel("Probability of being at 0")
plt.plot(x, probs)
plt.show()

# plt.plot(x2, y)
# plt.show()


# print(prob[n])
# print(prob)
# print(normalise)
# prob = np.abs((final_state[0] + final_state[n + 1]) / normalise)**2
# print(prob)
