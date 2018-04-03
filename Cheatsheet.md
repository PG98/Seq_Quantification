# Cheatsheet

* 显示上G目录大小
    - du -h --max-depth=1 |grep 'G' |sort
* 显示当前目录和文件大小(a: all files; h: human-being; s:summarize) )
    - du -ahs
    - 文件个数  ls -l |grep "^-"|wc -l
    - 目录个数 ls -l |grep "^d"|wc -l
    - 包括子文件夹 ls -lR|grep "^-"|wc -l


* ls
    - ls -al
    - ls -l
* ps
    - ps-aux | grep <name>
    - ps -ef
* kill 
    - kill -s 9 PID
    - kill CONT PID
* 查看特定几行
    - sed -n '1,10p' SRR1294727_1.fastq 
    - grep -n string file
* time
    - from time import strftime,gmtime
      strftime("%m/%d/%Y %H:%M")