import csv
userDir = 'c:\\Users\\kglas\\Downloads\\'
fileName = 'Secondary DM Summer Interest Form.csv'
header = "*****************************************************************"
with open(userDir + fileName, newline='') as csvfile:
    reader = csv.reader(csvfile)
    count = 0
    for row in reader:
        print(header)
        print("Name:%s Mentor:%s Participate:%s BME:%s" % (row[2], row[3], row[4], row[5]))
        print("Choice 1:", row[6])
        print("Choice 2:", row[7])
        print("Choice 3:", row[8])
        print("Choice 4:", row[9])
        print("Choice 5:", row[10])
        print(header)
        print("")
        count+=1
    print(count)
