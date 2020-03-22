import pkg_resources
from subprocess import call
x = pkg_resources.working_set.by_key
s = ""
for v in x:
    s += str(v) + " "
print("PIP Libraries to upgrade:", s)
call("pip install --upgrade " + s, shell=True)