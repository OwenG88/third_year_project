import SAT 
import random

def TRY(formula):
    assignment = [random.randint(0, 1) for i in range(formula.n)]
    for i in range(3 * formula.n):
        if formula.check_satisfied(assignment):
            return assignment
        else:
            unsat_clause = formula.unsatisfied_clause 
            x = random.choice(list(map(abs,unsat_clause))) - 1
            assignment[x] = 1 - assignment[x]
    return None 

def schoning(formula):

    # Can be run with Schöning's calculated lower bound
    # I = 30 * (2 * (formula.k - 1) / formula.k) ** formula.n
    while True:
        assignment = TRY(formula)
        if assignment != None:
            return assignment


# formula  = SAT.SAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])
# print(schoning(formula))
# print(formula.counter)
