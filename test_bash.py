import subprocess

#a = subprocess.run('uptime', shell=True, executable="/bin/bash")
#print(a)

rez = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
print(type(rez.stdout))