import os
existing = ['SRR1294905', 'SRR1294941', 'SRR1294954', 'SRR1294980', 'SRR1295114', 'SRR1295173', 'SRR1295351', 'SRR1295352']
for file in os.listdir(): 
	if file in existing:
		continue
	str = ('rm -f %s'%file)
	if(file[0:2] == 'SRR')
		os.system(str)


# for file in os.listdir(): 
# 	if file in existing:
# 		continue
# 	str = ('scp %s sjchen@...'%file)
# 	os.system(str)
#         #args=shlex.split(str)
#         #p=subprocess.Popen(args, stdin=subprocess.PIPE)
#         #p.stdin.flush()
#         #password = 'PASSWORD'+'\n'
#         #p.stdin.write(password.encode())