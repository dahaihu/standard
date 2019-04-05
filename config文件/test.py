from configparser import ConfigParser

cp = ConfigParser()
# cp.read('CompleteBinary.py.cfg')
# print(cp.get("mysql", "HOST"))
# print(cp.getint('mysql', "PORT"))
# cp.set("mysql", "PORT", "10")
# print(cp.getint("mysql", "PORT"))
# cp.write(open("CompleteBinary.py.cfg", 'w'))

cp.read('CompleteBinary.py.cfg')
print(cp.get("mysql", "PORT"))
