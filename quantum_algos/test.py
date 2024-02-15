import QSAT 
import random
import numpy as np

def qwalk(formula):

    n = formula.n
    ## Grover Coin
    G = (2 / n) * np.ones((n, n)) - np.eye(n)
    I = np.eye(2 ** n)
    G_I = np.kron(G, I)
    print(G_I.shape)
    S = np.zeros((n * 2**n, n * 2**n))

    for i in range(n):
        a = [0 for i in range(n)]
        e_a = ["0" for i in range(n)]
        e_a[a] = "1"
        index = int("".join(e_a),2)
        for j in range(2**n):
            # v = bin(v).replace("0b", "").zfill(n)
            # v = np.array([int(i) for i in v])

            v_ea = j ^ 
       
            a_v = np.array([a, v])
            
            a_v_ea = np.array([a, v_ea])

            # print(a_v.shape)
            # print(a_v_ea.shape)
            # print(np.outer(a_v, a_v_ea).shape)

            S += np.outer(a_v, a_v_ea)

    # coin_space = np.array([0 for i in range(n)])
    # position_space = np.array([0 for i in range(2 ** n)])
    # states = np.kron(coin_space, position_space)

    # for a in range(n):
    #     for v in range(2 ** n):


    print(states.shape)

    # print(S.shape)
    print(G_I.shape)
    print(S)
    U = S @ G

    print(U)
    ## From Quantum Walks and Search Algortihms textbook
    ## We know optimal time of when we should measure
    t_opt = int((np.pi / 4) * np.sqrt(2 * (2 ** n)))


    ## Pick a random assignment
    assignment = np.array([random.randint(0, 1) for i in range(n)])

    

    return None



formula  = QSAT.QSAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])
assignment = qwalk(formula)
print(assignment)
print(formula.counter)