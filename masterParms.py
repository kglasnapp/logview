import json
fileName = "masterParms.json"
   
def saveMaster():
    global master
    print(master)
    with open(fileName, 'w') as f:
        f.write(json.dumps(master))

def restoreMaster():
    global master
    try:
        with open(fileName) as f:
            master = json.loads(f.read())
        return master
    except:
        master = {}
        saveMaster()

def set(parm, value):
    global master
    master.update({parm : value})
    print("Master %s update %s" % (parm, str(value)))
    saveMaster()
    
def get(parm):
    global master
    return master.get(parm)

def get(parm, default):
    global master
    if master.get(parm) != None:
        return master.get(parm)
    else:
       set(parm, default)
       return default    
