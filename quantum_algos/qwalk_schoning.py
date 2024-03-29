import qutip as qt
import numpy as np
import random
import QSAT
import generate_instances


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
            

def get_vars_from_unsat_clause(formula, assignment):
    unsat_clauses = []
    for clause in formula.clauses:
        for literal in clause:
            if assignment[abs(literal) - 1] * literal > 0:
                break
        else:
            unsat_clauses += [*map(abs,clause)]
    
    return list(set(unsat_clauses))

def qwalk_oracle(formula):
    n = formula.n
    ## Create the Grover Coin
    G = qt.Qobj((2 / n) * np.ones(n) - np.eye(n))

    ## Create the position space in a diagonal state
    ##position_space = qt.basis(2 ** n, 0)
    position_space = qt.Qobj((1 / np.sqrt(2**n)) * np.ones((2**n, 1)))
    ## Create the coin space in a diagonal state
    coin_space = qt.Qobj((1 / np.sqrt(n)) * np.ones((n, 1)))
    ## Create the initial state
    initial_state = qt.tensor(coin_space, position_space)
    ## Create the Grover Coin operator
    G_I = qt.tensor(G, qt.qeye(2 ** n))
 
    ## Create the shift operator
    S = qt.Qobj(np.zeros((n * 2 ** n, n * 2 ** n),dtype=complex))
    S_og = S.copy()
    # print(qt.basis(n, 1))
    for j in range(2 ** n):
         #Our position vector
        v = qt.basis(2 ** n, j)
        
        ##Get the vertex in assignment form
        vertex = list(map(int,bin(j)[2:].zfill(n)))
        possible_edges = get_vars_from_unsat_clause(formula, vertex)
        complement = [i for i in range(1, n + 1) if i not in possible_edges]
        # print(possible_edges, complement)
        for edge in possible_edges:
            #Our coin vector
            a = qt.basis(n, edge - 1)

            #This is the edge we are taking on the hypercube
            x = ["0" for _ in range(n)]
            x[edge - 1] = "1" 
            index = int("".join(x), 2)
            ## After we take a particular edge
            v_ea = qt.basis(2 ** n, j ^ index)

            ##Take the relevant tensor products
            e_av = qt.tensor(a, v_ea)
            a_v = qt.tensor(a, v).dag()

            partial =  e_av *a_v
            partial = qt.Qobj(partial.data.toarray())
            # print(partial)  
            # break


            # for l in partial.data.toarray():
            #     for k in l:
            #         if k!=0:
            #             print(k,end=" ")
            #     print()

            S += partial
            S_og += partial

        for non_edge in complement:
            # print("here")               
            a = qt.basis(n, non_edge - 1)

            #This is the edge we are taking on the hypercube
            x = ["0" for _ in range(n)]
            x[non_edge - 1] = "1" 
            index = int("".join(x), 2)
            ## After we take a particular edge
            v_ea = qt.basis(2 ** n, j ^ index)

            ##Take the relevant tensor products
            e_av = qt.tensor(a, v_ea)
            a_v = qt.tensor(a, v).dag()

            partial =  e_av *a_v
            # partial =  e_av * e_av.dag()
            # partial = a_v.dag() * a_v
            partial = qt.Qobj(partial.data.toarray())
            # print(partial)
            S += 1j * partial

            # for l in partial.data.toarray():
            #     for k in l:
            #         if k!=0:
            #             print(k,end=" ")
    #         #     print()


    # for i in S.data.toarray():
    #     for j in i:
    #         if j != 0:
    #             print(int(j),end=" ")
    # print()
    check = S * S.dag() # # print(check)
    # check = np.matrix(S.data.toarray()) 
    # check_copy = check.copy().conj().T
    # check = check @ check_copy
    # print(check)
    # # check = S.data.toarray()
    check = check.data.toarray()
    for i in check:
        for j in i:
            print(int(j),end=" ")
        print()
            
    ##Check S and S_og 
    # for i,j in zip(S.data.toarray(), S_og.data.toarray()):
    #     for k,l in zip(i,j):
    #         if k != l:
    #             print("Not equal")
    #             print(k,l)


    ## Easier to work with numpy arrays
    S = S.data.toarray()
 
    G_I = G_I.data.toarray()
    initial_state = initial_state.data.toarray()
    ## Create the evolution operator
    U = S @ G_I

    # print(U)


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
        vertex = qt.basis(2 ** n, index)
        state = qt.tensor(coin_space, vertex)
        partial = 2 * state * state.dag()
        partial = partial.data.toarray()
        R -= partial

    U = U @ R
    
    ## Get the optimal time
    #t_opt = int((np.pi / 4) * np.sqrt(2 * (2 ** n))) 
    t_opt = int((np.pi / 4) * np.sqrt(4 * ((4/3) ** n))) 
    # t_opt = int(np.sqrt(np.sqrt(np.sqrt(2 ** n))))

    ## Simulate the evolution
    Ut = np.linalg.matrix_power(U, t_opt)
    initial_state = Ut @ initial_state

    
    ## Get the non-zero states out
    states = []
    for i in range(len(initial_state)):
        state = initial_state[i][0]
        if state != 0:
            states.append([i, state])


    ## Normalise the states
    normalisation = np.sqrt(sum([i[1] ** 2 for i in states])) 
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


formula_fixed  = QSAT.QSAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])

list_rounds = []
n_trials = 1
n = 3
for i in range(n_trials):
    formula = generate_instances.gen_formula(n)
    formula.clauses = formula.clauses[::4]
    assignment, rounds = qwalk_oracle(formula)
    list_rounds.append(rounds)
    # if i % (n_trials // 10) == 0:
    #     print(F"Trial {i} completed")
    
print("Average rounds: ", sum(list_rounds) / n_trials)

# t_opt = int((np.pi / 4) * np.sqrt(2 * (2 ** n))) 
# print(t_opt)
# t_opt = int((np.pi / 4) * np.sqrt(4 * ((4/3) ** n))) 
# print(t_opt)