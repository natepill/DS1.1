import csv

'''Pure Python way to find out how many women survived on the titanic'''

with open('titanic.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    survived_count = 0
    for row in csv_reader:
        print('row[1]:',row[1])
        print('row[4]:',row[4])
        if row[1] == '1' and row[4] == 'female':
            survived_count += 1
print(survived_count)




# with open('titanic.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     survived_count = 0
#     for row in csv_reader:
#         print(row)
