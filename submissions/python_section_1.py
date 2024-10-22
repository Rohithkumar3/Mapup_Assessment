#Q1
def reverse_in_groups(lst, n):
    result = []
    for i in range(0, len(lst), n):
        group = []
        
        for j in range(i, min(i + n, len(lst))):
            group.append(lst[j])
       
        for j in range(len(group) - 1, -1, -1):
            result.append(group[j])
    return result
print('Reverse List:')
print(reverse_in_groups([1, 2, 3, 4, 5, 6, 7, 8], 3))
print(reverse_in_groups([1, 2, 3, 4, 5], 2))
print(reverse_in_groups([10, 20, 30, 40, 50, 60, 70], 4))


#Q2
def group_by_length(strings):
    result = {}
    
    for string in strings:
        length = len(string)
        
        if length not in result:
            result[length] = []
      
        result[length].append(string)    
    return dict(sorted(result.items()))

print('\nLists & Dictionaries:')
print(group_by_length(["apple", "bat", "car", "elephant", "dog", "bear"]))
print(group_by_length(["one", "two", "three", "four"]))


#Q3
def flatten_dict(d, parent_key='', sep='.'):
    flattened = {}

    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):
            flattened.update(flatten_dict(value, new_key, sep=sep))
        elif isinstance(value, list):
    
            for i, item in enumerate(value):
                flattened.update(flatten_dict({f"{new_key}[{i}]": item}, '', sep=sep))
        else:
            flattened[new_key] = value

    return flattened

nested_dict = {
    "road": {
        "name": "Highway 1",
        "length": 350,
        "sections": [
            {
                "id": 1,
                "condition": {
                    "pavement": "good",
                    "traffic": "moderate"
                }
            }
        ]
    }
}

flattened_dict = flatten_dict(nested_dict)
print('\nFlatten a Nested Dictionary:')
print(flattened_dict)

#Q4
def unique_permutations(nums):
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:]) 
            return
        
        seen = set() 
        for i in range(start, len(nums)):
            if nums[i] not in seen: 
                seen.add(nums[i])
               
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                
                nums[start], nums[i] = nums[i], nums[start]
    nums.sort()
    result = []
    backtrack(0)
    return result

input_list = [1, 1, 2]
output = unique_permutations(input_list)
print('\nGenerate Unique Permutations:')
for perm in output:
    print(perm)

#Q5
import re

def find_all_dates(text):
    date_pattern = r'\b\d{2}-\d{2}-\d{4}\b|\b\d{2}/\d{2}/\d{4}\b|\b\d{4}\.\d{2}\.\d{2}\b'

    dates = re.findall(date_pattern, text)
    
    return dates

text = "I was born on 23-08-1994, my friend on 08/23/1994, and another one on 1994.08.23."
output = find_all_dates(text)
print('\nFind Dates:')
print(output)


#Q7
def rotate_and_transform(matrix):
    n = len(matrix)
    rotated_matrix = [[0]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            rotated_matrix[j][n-i-1] = matrix[i][j]

    final_matrix = [[0]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated_matrix[i]) 
            col_sum = sum(rotated_matrix[k][j] for k in range(n)) 
            final_matrix[i][j] = row_sum + col_sum - 2 * rotated_matrix[i][j]

    return final_matrix

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
result = rotate_and_transform(matrix)
print('\nMatrix Rotation and Transformation:')
for row in result:
    print(row)

   

#Q8
import pandas as pd

def check_time_coverage(df: pd.DataFrame) -> pd.Series:
    df['startTime'] = pd.to_datetime(df['startTime'], format='%H:%M:%S').dt.time
    df['endTime'] = pd.to_datetime(df['endTime'], format='%H:%M:%S').dt.time
   
    grouped = df.groupby(['id', 'id_2'])
   
    def check_completeness(group):
        unique_days = set(group['startDay']).union(set(group['endDay']))
        time_covered = (group['startTime'].min() == pd.to_datetime('00:00:00').time() and
                        group['endTime'].max() == pd.to_datetime('23:59:59').time())
       
        days_covered = len(unique_days) == 7
        return not (days_covered and time_covered)

    result = grouped.apply(check_completeness)
   
    return result

df = pd.read_csv("C:\\Users\\gande\\OneDrive\\Desktop\\Mapup\\MapUp-DA-Assessment-2024\\submissions\\dataset-1.csv")
result = check_time_coverage(df)
print('\nTime check:')
print(result)

   



