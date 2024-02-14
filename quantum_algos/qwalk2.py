import qutip as qt
import numpy as np
import random
import QSAT

def qwalk2(formula):
    n = formula.n
    ## Create the Grover Coin
    G = (2 / n) * qt.qeye(n) - qt.qeye(n)
    ## Create the position space
    position_space = qt.basis(2 ** n, random.randint(0, 2 ** n - 1))
    ## Create the coin space in a diagonal state
    coin_space = qt.Qobj((1 / np.sqrt(n)) * np.ones((n, 1)))
    ## Create the initial state
    initial_state = qt.tensor(coin_space, position_space)
    ## Create the Grover Coin operator
    G_I = qt.tensor(G, qt.qeye(2 ** n))

    ## Create the shift operator
    S = qt.Qobj(np.zeros((n * 2 ** n, n * 2 ** n)))
    for i in range(n):
        #Our coin vector
        a = qt.basis(n, i)

        #This is the edge we are taking on the hypercube
        x = ["0" for _ in range(n)]
        x[i] = "1" 
        index = int("".join(x), 2)


        for j in range(2 ** n):
            
            #Our position vector
            v = qt.basis(2 ** n, j)

            ## After we take a particular edge
            v_ea = qt.basis(2 ** n, j ^ index)

            ##Take the relevant tensor products
            e_av = qt.tensor(a, v_ea)
            a_v = qt.tensor(a, v).dag()

            partial =  e_av *a_v
            partial = qt.Qobj(partial.data.toarray())

            S += partial

    ## Easier to work with numpy arrays
    S = S.data.toarray()
    G_I = G_I.data.toarray()
    initial_state = initial_state.data.toarray()
    ## Create the shift operator
    U = S @ G_I
    
    ## Get the optimal time
    t_opt = int((np.pi / 4) * np.sqrt(2 * (2 ** n))) + 1

    Ut = np.linalg.matrix_power(U, t_opt)
    
    initial_state = Ut @ initial_state


    states = []
    for i in range(len(initial_state)):
        state = initial_state[i][0]
        if state != 0:
            states.append([i, state])

    normalisation = np.sqrt(sum([i[1] ** 2 for i in states])) 
    states = [[i[0], i[1] / normalisation] for i in states]

    state = random.choices(states, weights=[i[1] ** 2 for i in states])
    
    assignment = bin(state[0][0] % (2** n))[2:].zfill(n)
    assignment = list(map(int, assignment))
    if formula.check_satisfied(assignment): 
        return assignment

    return None


formula  = QSAT.QSAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])


assignment = None
while assignment == None:
     assignment = qwalk2(formula)

print(assignment)
print(formula.counter)