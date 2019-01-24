import re

# Redo using a csv reader

female_pattern = re.compile(r'female')
alive_pattern = re.compile(r'\d,1,\d')

with open('titanic.csv', 'r') as file:
    count = 0
    for line in file:
        if re.search(female_pattern, line) != None and re.search(alive_pattern, line):
            count += 1

print(count)
