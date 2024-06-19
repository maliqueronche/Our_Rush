import matplotlib.pyplot as plt
import pandas as pd

# Load CSV file
file_path = 'random_results_20000.csv'
data = pd.read_csv(file_path, header=None)

numbers = data.values.flatten()

minimum_value = numbers.min()
maximum_value = numbers.max()
mean_value = numbers.mean()

print(f"Minimum value: {minimum_value}")
print(f"Maximum value:{maximum_value}")
print(f"Mean value: {mean_value}")

# Histogram
plt.figure(figsize=(10, 6))
plt.hist(numbers, bins=50, edgecolor='black')
plt.title('Distribution for number of iterations')
plt.xlabel('Number of iterations')
plt.ylabel('Frequency')
plt.xlim(left=0)
plt.show()
