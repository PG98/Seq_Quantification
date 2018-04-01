# Cheatsheet

* 显示上G目录大小
    - du -h --max-depth=1 |grep 'G' |sort
* 显示当前目录和文件大小(a: all files; h: human-being; s:summarize) )
    - du -ahs
* ls
    - ls -al
    - ls -l
* ps
    - ps-aux | grep <name>
    - ps -ef
* kill 
    - kill -s 9 PID
    - kill CONT PID
