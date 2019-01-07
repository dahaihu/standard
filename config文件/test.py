from configparser import ConfigParser

cp = ConfigParser()
# cp.read('test.cfg')
# print(cp.get("mysql", "HOST"))
# print(cp.getint('mysql', "PORT"))
# cp.set("mysql", "PORT", "10")
# print(cp.getint("mysql", "PORT"))
# cp.write(open("test.cfg", 'w'))

cp.read('test.cfg')
print(cp.get("mysql", "PORT"))
