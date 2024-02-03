import numpy as np 

##Initialise the overall lists
rw_means = []
rw_unsat_means = []
schoning_means = []

rw_stds = []
rw_unsat_stds = []
schoning_stds = []

rw_medians = []
rw_unsat_medians = []
schoning_medians = []

##Get SAT algorithms data
for i in range(1, 6):

    ##Load the data
    rw_attempts = np.loadtxt(f"simulation_data/rw_attempts{i}.txt")
    rw_unsat_attempts = np.loadtxt(f"simulation_data/rw_unsat_attempts{i}.txt")
    schoning_attempts = np.loadtxt(f"simulation_data/schoning_attempts{i}.txt")

    ##Get the mean of the data
    rw_mean = np.mean(rw_attempts)
    rw_unsat_mean = np.mean(rw_unsat_attempts)
    schoning_mean = np.mean(schoning_attempts)

    ##Get the standard deviation of the data
    rw_std = np.std(rw_attempts)
    rw_unsat_std = np.std(rw_unsat_attempts)
    schoning_std = np.std(schoning_attempts)

    ##Get the median of the data
    rw_median = np.median(rw_attempts)
    rw_unsat_median = np.median(rw_unsat_attempts)
    schoning_median = np.median(schoning_attempts)

    ##Append the data to the overall lists
    rw_means.append(rw_mean)
    rw_unsat_means.append(rw_unsat_mean)
    schoning_means.append(schoning_mean)

    rw_stds.append(rw_std)
    rw_unsat_stds.append(rw_unsat_std)
    schoning_stds.append(schoning_std)

    rw_medians.append(rw_median)
    rw_unsat_medians.append(rw_unsat_median)
    schoning_medians.append(schoning_median)

    print(f"Run {i} Results:")
    print()
    print(f"Random Walk Average Steps: {rw_mean}")
    print(f"Random Walk Standard Deviation: {rw_std}")
    print(f"Random Walk Median: {rw_median}")
    print()
    print(f"Random Walk Unsat Average Steps: {rw_unsat_mean}")
    print(f"Random Walk Unsat Standard Deviation: {rw_unsat_std}")
    print(f"Random Walk Unsat Median: {rw_unsat_median}")
    print()
    print(f"Schoning Average Steps: {schoning_mean}")
    print(f"Schoning Standard Deviation: {schoning_std}")
    print(f"Schoning Median: {schoning_median}")
    print()


average = lambda x: (sum(x) - min(x) - max(x)) / (len(x) - 2)

print(f"Overall Results:")
print()
print(f"Random Walk Average Steps: {average(rw_means)}")
print(f"Random Walk Standard Deviation: {average(rw_stds)}")
print(f"Random Walk Median: {average(rw_medians)}")
print()
print(f"Random Walk Unsat Average Steps: {average(rw_unsat_means)}")
print(f"Random Walk Unsat Standard Deviation: {average(rw_unsat_stds)}")
print(f"Random Walk Unsat Median: {average(rw_unsat_medians)}")
print()
print(f"Schoning Average Steps: {average(schoning_means)}")
print(f"Schoning Standard Deviation: {average(schoning_stds)}")
print(f"Schoning Median: {average(schoning_medians)}")
print()


