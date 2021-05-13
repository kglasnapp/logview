import csv
userDir = 'c:\\Users\\kglas\\Downloads\\'
fileName = '2021 Summer Program Survey.csv'
header = "*****************************************************************"
with open(userDir + fileName, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(header)
        print("Name:%s %s Mentor:%s Interested:%s" %
              (row[1], row[2], row[4], row[5]))
        print("Topics:", row[6])
        print("Software:", row[7])
        print("Other:", row[8])
        print("Teach:", row[9])
        print(header)
        print("")
