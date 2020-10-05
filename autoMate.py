import urllib.request
# Create an OpenerDirector with support for Basic HTTP Authentication...
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='',
                          uri='https://https://accountaccess.edwardjones.com/ca-logon/logon.action?MobileSiteInd=N',
                          user='kglasnapp',
                          passwd='++++++++')
opener = urllib.request.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
urllib.request.install_opener(opener)
f = urllib.request.urlopen('https://onlineaccess.edwardjones.com/app/snapshot')
print(f.read(10000).decode('utf-8'))