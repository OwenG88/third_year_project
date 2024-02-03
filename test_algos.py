import rw_SAT
import schoning
import SAT


def test_sat_algo(algo):
    n_attempts = []
    for i in range(1,1001):
        with open(f"testing_instances/uf20-0{i}.cnf") as f:
            lines = f.readlines()
            ##Skip header
            lines = lines[8:]
            clauses = []
            for line in lines:
                l = line.split()
                if l[0] == "%":
                    break
                clause = list(map(int, l[:-1]))
                clauses.append(clause)
        f.close()

        formula = SAT.SAT(clauses)
        if i % 10 == 0:
            print(f"Started solving {i}")
        assignment = algo(formula)
        if assignment == None:
            print(f"Failed to solve {i}")

        n_attempts.append(formula.counter)
    return n_attempts

mean = lambda x: round(sum(x)/len(x),2)
rw_attempts = test_sat_algo(rw_SAT.walk)
schoning_attempts = test_sat_algo(schoning.schoning)
print(f"Random Walk Average Steps: {mean(rw_attempts)}")
print(f"Schoning Average Steps: {mean(schoning_attempts)}")


## Write attempts to file
with open("rw_attempts.txt", "w") as f:
    f.write("\n".join(map(str, rw_attempts)))
f.close()

with open("schoning_attempts.txt", "w") as f:
    f.write("\n".join(map(str, schoning_attempts)))
f.close()
