import SAT 
import random

def walk(formula):
    assignment = [random.randint(0, 1) for _ in range(formula.n)]
    while True:
        if formula.check_satisfied(assignment):
            return assignment
        else:
            x = random.randrange(formula.n)
            assignment[x] = 1 - assignment[x]


formula  = SAT.SAT([[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3]])
assignment = walk(formula)
print(assignment)
print(formula.counter)
