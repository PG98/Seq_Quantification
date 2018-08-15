# Linux configuration

## Basic software installation
* Using **yum**
```
# vim, dpkg, apt-get, R, axel...
yum install apt-get
```

* Set up zshell
[oh-my-zsh](http://ohmyz.sh/)
```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
The configuration is under ~/.zshrc. Plugins and themes under ~/.oh-my-zsh.

## Anaconda
* Add domestic channels, e.g.:
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/linux-64 
```

## Jupyter notebook
* Remote via ssh tunnel
```
ssh -L 8888:localhost:8888  <serverAddress>
```




