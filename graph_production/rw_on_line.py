from matplotlib import pyplot as plt 
import numpy as np
import random


n_trials = 1_000_000
time_steps = 100
movements = []
for i in range(n_trials):
    movements.append(sum(random.choice([1,-1]) for _ in range(time_steps)))

x = [i for i in range(-time_steps, time_steps+1, 2)]
y = [movements.count(i) / n_trials for i in x]


plt.plot(x, y)
plt.xlabel("Position")
plt.ylabel("Probability")
plt.title("Probability Distribution of a Classical Random Walk")
plt.show()
