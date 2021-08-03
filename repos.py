import requests

def getRepos(repro):
    # git clone https://thedirtymechanics.com/bitbucket/scm/rob20/2020testchasis2.git
    s = repro.rfind("/")
    link = reprosLink.replace("****", repro[s+1:])
    r = requests.get(link, headers={'User-Agent': agent}, auth=auth)
    #print("Result:", r)
    s = r.json()
    for l in s['values']:
        for t in l['links']['clone']:
            if t['name'] == 'http':
                print("git clone ", t['href'])
pw = 'Kag...' 

auth = ('kglasnapp', pw)
projectLink = "https://thedirtymechanics.com/bitbucket/rest/api/1.0/projects"
reprosLink = "https://thedirtymechanics.com/bitbucket/rest/api/1.0/projects/****/repos"
agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
r = requests.get(projectLink, headers={'User-Agent': agent}, auth=auth)
#print("Result:", r)
s = r.json()
for l in s['values']:
    project = l['links']['self'][0]['href']
    #print("** project ** ", project)
    getRepos(project)
