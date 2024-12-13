import csv
from collections import Counter

def map_reduce_csv(file_path):
    values = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 8: 
                values.append(row[7])

   
    counts = Counter(values)
    
    return counts

if __name__ == "__main__":
   
    file_path = "saida.csv"
    result = map_reduce_csv(file_path)
    
    for value, count in result.items():
        print(f"{value}: {count}")
