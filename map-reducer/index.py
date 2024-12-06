from functools import reduce
from collections import defaultdict

# input data
data = ["cat", "dog", "cat", "bird"]

# map by count ocurrences creating an key-value pair
def map_function(data):
  return (data, 1)

# Fase Reduce
def reduce_function(key, values):
  return (key, sum(values))

# Create a list of count
mapped = list(map(map_function, data))

# Shuffle and Sort: Group by key
group = defaultdict(list)
for key, value in mapped:
  group[key].append(value)

print('group.items()', group.items())
result = [reduce_function(k, v) for k, v in group.items()]

print(result)
