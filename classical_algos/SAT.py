import numpy as np
class SAT: 
    ## Class to represent a SAT formula
    ## Literals are integers (positive or negative)
    ## Will assume for n variables 
    ## Literals are in [-n , n]

    def __init__(self, clauses):
        ## 2D list of clauses
        self.clauses = clauses
        self.m = len(clauses)
        self.k = len(clauses[0])
        self.n = self.get_num_vars()
        self.counter = 0
        self.seen_before = set()
    
    def read_file(self, filename):
        ## Read in a file and create a SAT formula
        ## File is a list of clauses
        ## Each clause is a list of literals
        ## Literals are integers (positive or negative)
        ## Will assume for n variables 
        ## Literals are in [-n , n]
        with open(filename) as f:
            lines = f.readlines()
        clauses = []
        for line in lines[8:]:
            clause = []
            for literal in line.split():
                clause.append(int(literal))
            clauses.append(clause)
        self.clauses = clauses
        self.m = len(clauses)
        self.k = len(clauses[0])
        self.n = self.get_num_vars()
        self.counter = 0

    def get_num_vars(self):
        ## Get the number of variables in the formula
        vars = set()
        for clause in self.clauses:
            for literal in clause:
                vars.add(abs(literal))
        return len(vars)
    
    def check_satisfied(self, assignment):
        ## Check if the assignment satisfies the formula
        ## Assignment is a list of 0s and 1s
        self.counter += 1
        if tuple(assignment) in self.seen_before:
            return False
        
        for clause in self.clauses:
            satisfied = False
            for literal in clause: 
                assigned_value = assignment[abs(literal) - 1]
                if literal > 0 and assigned_value == 1:
                    satisfied = True
                    break
                elif literal < 0 and assigned_value == 0:
                    satisfied = True
                    break
            if not satisfied:
                self.unsatisfied_clause = clause
                self.seen_before.add(tuple(assignment))
                return False
        return True
            
            