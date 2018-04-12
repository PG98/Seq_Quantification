import multiprocessing
import subprocess

from multiprocessing import Pool

def task(cmd):
    # 返回输出流和错误流
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
    out,err=p.communicate()
    return (out,err)

pool= Pool(processes=5)
results = []

# 根据需要 改循环条件和shell命令
for i in range(1,16):
    cmd = "echo %d && sleep 5s"% i
    # apply_async() 函数非阻塞且支持结果回调，存储到数组中
    # 非阻塞，完成顺序未必有序但其日志有序
    results.append(pool.apply_async(task, args=(cmd,)))

pool.close()
pool.join() #主进程阻塞等待子进程完成

# 将 binary format 的 stdout/stderr 格式化输出，方便重定向查看日志
for result in results:
    out,err = result.get()
    if err.decode()=="":
        print("out: {}".format(out.decode() ))
    else:
        print("out: {}err: {}".format(out.decode(), err.decode() ))