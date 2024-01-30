import SAT 
import random

def TRY(formula):
    assignment = [random.randint(0, 1) for i in range(formula.n)]
    for i in range(3 * formula.n):
        if formula.check_satisfied(assignment):
            return assignment
        else:
            x = random.randrange(formula.n)
            assignment[x] = 1 - assignment[x]
    return None 

def schoning(formula):
    I = (2 * (formula.k - 1) / formula.k) ** formula.n
    for i in range(int(I)):
        assignment = TRY(formula)
        if assignment != None:
            return assignment
    return None

formula  = SAT.SAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])
print(schoning(formula))
print(formula.counter)
