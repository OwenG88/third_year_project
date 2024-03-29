import qutip as qt
import numpy as np
import random
import QSAT
import generate_instances
from numba import njit

###Builds on qwalk.py but uses oracle calls to modify the evolution 
###operator to bias towards satisfying assignments


def compute_sat_assignments(formula):
    ## Generate a list of all satisfying assignments
    ## of a given SAT formula

    n = formula.n
    assignments = []

    for i in range(2**n):
        assignment = bin(i)[2:].zfill(n)
        assignment = list(map(int, assignment))
        if formula.check_satisfied(assignment):
            assignments.append(assignment)
    
    return assignments
            
@njit(fastmath=True, cache=True)
def speed_prod(a, v, v_ea):
    e_av = np.kron(a, v_ea) 
    a_v = np.kron(a, v).conj().T
    return np.outer(e_av, a_v)



def qwalk_oracle(formula):
    n = formula.n
    ## Create the Grover Coin
    H = qt.Qobj(0.5 * np.array([[1, 1], [1, -1]]))
    G = (2 / n) * np.ones(n) - np.eye(n)
    # G = qt.tensor(H, H)

    ## Create the position space in a diagonal state
    position_space = (1 / np.sqrt(2**n)) * np.ones((2**n, 1))
    ##position_space = qt.basis(2 ** n, 0)
    ## Create the coin space in a diagonal state
    coin_space = (1 / np.sqrt(n)) * np.ones((n, 1))
    ## Create the initial state
    # initial_state = qt.tensor(coin_space, position_space)
    # print(initial_state)
    initial_state = np.kron(coin_space, position_space)
    ## Create the Grover Coin operator
    G_I = np.kron(G,np.eye(2 ** n))

    ## Create the shift operator
    S = np.zeros((n * 2 ** n, n * 2 ** n))

    # print("Initial objects made")
    for i in range(n):
        #Our coin vector
        # a = qt.basis(n, i)
        a = np.zeros(n)
        a[i] = 1

        #This is the edge we are taking on the hypercube
        x = ["0" for _ in range(n)]
        x[i] = "1" 
        index = int("".join(x), 2)

        v = np.zeros(2 ** n)
        v_ea = np.zeros(2 ** n)
        for j in range(2 ** n):
            
            #Our position vector
            # v = qt.basis(2 ** n, j)
            
            v[j] = 1

            ## After we take a particular edge
            # v_ea = qt.basis(2 ** n, j ^ index)

            v_ea[j ^ index] = 1

            ##Take the relevant tensor products
            # e_av = qt.tensor(a, v_ea)
            # a_v = qt.tensor(a, v).dag()

            # e_av = np.kron(a, v_ea) 
            # # print(e_av)
            # a_v = np.kron(a, v).conj().T
            # # print()
            # # print(a_v)
            # partial =  np.outer(e_av, a_v)
            # print(partial)
            # # partial = qt.Qobj(partial.data.toarray())
            # print(a, v, v_ea)

            ###TODO work out how to optimise products 

            # if np.array_equal(v, v_ea):
            # # print(speed_prod(a, v, v_ea))
            # # break
            #     S += speed_prod(a, v, v_ea)
            
            # else: 
            #     k = np.zeros((n * 2 ** n, n * 2 ** n))
            #     assert np.array_equal(speed_prod(a, v, v_ea),k)

            S += speed_prod(a, v, v_ea)

            v[j] = 0
            v_ea[j ^ index] = 0
    
    # print("Shift operator made")
    print(S)
    ## Easier to work with numpy arrays
    # S = S.data.toarray()
    # G_I = G_I.data.toarray()
    # initial_state = initial_state.data.toarray()
    ## Create the evolution operator
    U = S @ G_I



    # for i in G:
    #     for j in i:
    #         print(int(j),end=" ")
    #     print()

    ## We modify the evolution operator to bias towards
    ## satisfying assignments.

    R = np.eye(n * 2 ** n, dtype=complex)

    assignments = compute_sat_assignments(formula)

    for assignment in assignments:
        index = int("".join(map(str, assignment)), 2)
        # vertex = qt.basis(2 ** n, index)
        # state = qt.tensor(coin_space, vertex)
        # partial = 2 * state * state.dag()
        # partial = partial.data.toarray()
        vertex = np.zeros(2 ** n)
        vertex[index] = 1
        state = np.kron(coin_space, vertex)
        partial = 2 * np.outer(state, state.conj())
        R -= partial

    U = U @ R

    # print("Evolution operator made")



    
    ## Get the optimal time
    t_opt = int((np.pi / 4) * np.sqrt(2 * (2 ** n))) 
    #t_opt = int((np.pi / 4) * np.sqrt(4 * ((4/3) ** n)))

    ## Simulate the evolution
    Ut = np.linalg.matrix_power(U, t_opt)
    initial_state = Ut @ initial_state
    # print(initial_state)
    # print("Evolution simulated")
    
    ## Get the non-zero states out
    states = []
    for i in range(len(initial_state)):
        state = initial_state[i][0]
        if state != 0:
            states.append([i, state])

    # print(len(states))

    ## Normalise the states
    normalisation = np.sqrt(sum([abs(i[1]) ** 2 for i in states])) 

    states = [[i[0], i[1] / normalisation] for i in states]

    assignment = None
    counter = 0

    while assignment == None:
        counter += 1
        ## Measure
        state = random.choices(states, weights=[abs(i[1]) ** 2 for i in states])
        
        ## Check the corresponding SAT assignment
        assignment = bin(state[0][0] % (2** n))[2:].zfill(n)
        assignment = list(map(int, assignment))
        if formula.check_satisfied(assignment): 
            return assignment, counter
        
        assignment = None
    return None


#formula  = QSAT.QSAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])

list_rounds = []
n_trials = 1
n = 3
for i in range(n_trials):
    formula = generate_instances.gen_formula(n)
    formula.clauses = formula.clauses[::2]
    assignment, rounds = qwalk_oracle(formula)
    list_rounds.append(rounds)
    if i % (n_trials // 10) == 0:
        print(F"Trial {i} completed")
    
print("Average rounds: ", sum(list_rounds) / n_trials)