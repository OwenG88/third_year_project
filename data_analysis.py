import numpy as np 


##Get SAT algorithms data
rw_attempts = np.loadtxt("rw_attempts.txt")
schoning_attempts = np.loadtxt("schoning_attempts.txt")

##Get the mean of the data
rw_mean = np.mean(rw_attempts)
schoning_mean = np.mean(schoning_attempts)

##Get the standard deviation of the data
rw_std = np.std(rw_attempts)
schoning_std = np.std(schoning_attempts)

##Get the median of the data
rw_median = np.median(rw_attempts)
schoning_median = np.median(schoning_attempts)

print(f"Random Walk Average Steps: {rw_mean}")
print(f"Random Walk Standard Deviation: {rw_std}")
print(f"Random Walk Median: {rw_median}")
print(f"Schoning Average Steps: {schoning_mean}")
print(f"Schoning Standard Deviation: {schoning_std}")
print(f"Schoning Median: {schoning_median}")