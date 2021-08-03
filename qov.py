import pysftp
import csv

myHostname = "home100302809.1and1-data.host"
myUsername = "u36269828-main"
myPassword = ""
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None   

def getFiles(dir):

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword,  cnopts=cnopts) as sftp:
        print("Connection succesfully stablished ... ")

        # Switch to a remote directory
        sftp.cwd('/QuiltsOfValor2/images/' + dir)

        # Obtain structure of the remote directory '/var/www/vhosts'
        directory_structure = sftp.listdir_attr()

        # Print data
        files = []
        for attr in directory_structure:
            print(attr.filename)
            files.append(attr.filename)

def getcsv(fileName, col):
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
           print(row(col))

