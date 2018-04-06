# Cheatsheet

* 显示上G目录大小
    - du -h --max-depth=1 |grep 'G' |sort
* 显示当前目录和文件大小(a: all files; h: human-being; s:summarize) )
    - du -ahs
    - 文件个数  ls -l |grep "^-"|wc -l
    - 目录个数 ls -l |grep "^d"|wc -l
    - 包括子文件夹 ls -lR|grep "^-"|wc -l
* ps
    - ps-aux | grep <name>
    - ps -ef
* tmux 
    - tmux # 新建
    - tmux ls
    - tmux attach-session -t <sessionName>
    - tmux detach(quit from current session but keep the job going)
* kill 
    - kill -s 9 PID
    - kill CONT PID
* grep
    - grep -n string file
* time
    - from time import strftime,gmtime
      strftime("%m/%d/%Y %H:%M")
* sed
    - sed -n '1,10p' SRR1294727_1.fastq 
    - sed -i '3d' file.txt  # delete 3rd line
    - sed -i '/TOBEDELETED/d' # delte line that includes 'TOBE..'
* awk (another solution to text files besides sed)
    - awk '!/7/' yourFile # 输出不带有'7'的行
    - awk 'BEGIN {OFS = "\n"} {header = $0 ; getline seq ; getline qheader ; getline qseq ; if (length(seq) != length(qseq)) {print header, seq, qheader, qseq, NR-3}}' yourFastq.fastq # 一种筛选方式
* 输出日志
    - ... > xxxx.log 2>&1

