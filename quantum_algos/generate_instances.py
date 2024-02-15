import QSAT 
import random

def gen_formula(n):
    ## Generate a random SAT formula
    ## with n variables and only one 
    ## satisfying assignment

    formula = []
    
    for i in range(2**n):
        assignment = bin(i)[2:].zfill(n)
        assignment = list(map(int, assignment))
        
        assignment = [(-1)**assignment[i] * (i + 1) for i in range(n)]
        formula.append(assignment) 
    
    random.shuffle(formula)
    formula.remove(random.choice(formula))
 
    formula = QSAT.QSAT(formula)

    return formula

