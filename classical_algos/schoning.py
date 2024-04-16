import SAT 
import random

def TRY(formula):
    assignment = [random.randint(0, 1) for i in range(formula.n)]
    for i in range(3 * formula.n):
        if formula.check_satisfied(assignment):
            return assignment
        else:
            x = random.choice(list(map(abs,formula.unsat_clause))) - 1
            assignment[x] = 1 - assignment[x]
    return None 

def schoning(formula):

    # Can be run with Schöning's calculated lower bound
    # I = 30 * (2 * (formula.k - 1) / formula.k) ** formula.n
    counter = 0
    while True:
        counter += 1
        assignment = TRY(formula)
        if assignment != None:
            return assignment, counter


# formula  = SAT.SAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])
# print(schoning(formula))
# print(formula.counter)
