#Recreating page 48 of
#http://ndl.ethernet.edu.et/bitstream/123456789/73178/1/277.pdf
#For a continuous time quantum random walk on the line

from matplotlib import pyplot as plt 
import numpy as np
from scipy import linalg

t = 100
n = 100
gamma = 1 / (2 * np.sqrt(2))

#The hamiltonian matrix is defined as follows
def hamiltonian(i, j):
    if i == j:
        return 2 * gamma 
    elif abs(i - j) == 1:
        return - gamma
    else:
        return 0

hamiltonian_matrix = [[hamiltonian(i, j) for j in range(2*n+1)] for i in range(2*n+1)]
hamiltonian_matrix = np.matrix(hamiltonian_matrix)

# Compute U(t) = e ^ (-i * H * t)
U_t = linalg.expm(-1j * hamiltonian_matrix * t)

# |psi(0)> = |0>
zero_state_vector = np.transpose(np.matrix([1 if i == n + 1 else 0 for i in range(2*n+1)])) 

# |psi(t)> = U(t) * |psi(0)>
psi = U_t * zero_state_vector

x_axis = [i for i in range(-n, n+1, 2)]
probability_distribution = np.square(np.abs(psi))

#Filter out odd positions 
probability_distribution = probability_distribution[::2]

plt.plot(x_axis, probability_distribution)
plt.xlabel("Position")
plt.ylabel("Probability")
plt.title("Probability Distribution of a Continuous Time Quantum-Walk")
plt.show()