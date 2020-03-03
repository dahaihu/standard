from fabric.api import local, roles, settings, prefix


def hello(name='test'):
	print name


def taskA():
	local("touch fab.out && echo 'fab' >> fab.out")


from fabric.api import run, env

# env.hosts = ['65.49.203.235']
# env.user = 'root'
# env.port = '26359'
# env.key_filename = '~/.ssh/id_rsa_fabric'

env.roledefs = {
	'online': ['root@65.49.203.235:26359'],
}

env.passwords = {
	'root@65.49.203.235:26359': "FY8a4ZjguSh3"
}


# @roles("online")
def taskB():
	with prefix("su hsc"):
		run("cd /root && ls")
