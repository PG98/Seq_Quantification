import multiprocessing
import subprocess

from multiprocessing import Pool

def task(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
    out,err=p.communicate()
    return (out,err)

pool= Pool(processes=5)
results = []

for i in range(1,16):
    cmd = "echo %d && sleep 5s"% i
    results.append(pool.apply_async(task, args=(cmd,)))

pool.close()
pool.join()

for result in results:
    out,err = result.get()
    if err.decode()=="":
        print("out: {}".format(out.decode() ))
    else:
        print("out: {}err: {}".format(out.decode(), err.decode() ))