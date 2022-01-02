#!/bin/bash -f
#echo "Running .bashrc ..."
#echo "Shell evnironment setting ..."
#echo ""

## ------------------------------------------------------
#    Common enviroment
## ------------------------------------------------------
umask 027               # file permission mask ; rwxr-x---
#export TMOUT=3600       # disable auto-logout
export TMOUT=0          # disable auto-logout

# don't put duplicate lines or lines starting with space in the history.
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend
shopt -s direxpand
#shopt -s dotglob

# for setting history length see HISTSIZE and HISTFILESIZE
HISTSIZE=100
HISTFILESIZE=100

#stty erase "^H" kill "^U" intr "^C"  eof "^D" susp "^Z" echoe
#stty sane

#POWERLINE_SCRIPT=/usr/share/powerline/bindings/bash/powerline.sh
#if [ -f $POWERLINE_SCRIPT ]; then
#  source $POWERLINE_SCRIPT
#fi

complete -cf sudo

########################################################
###        Edward Yeh's environment                  ###
########################################################
export TERM="xterm-256color"
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LS_COLORS="ow=33:no=00:fi=00:di=00;94:ln=00;36:pi=40;33:so=00;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:ex=00;32:*.cmd=00;32:*.exe=00;32:*.com=00;32:*.btm=00;32:*.bat=00;32:*.sh=00;32:*.csh=00;32:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.gz=00;31:*.bz2=00;31:*.bz=00;31:*.tz=00;31:*.rpm=00;31:*.cpio=00;31:*.jpg=00;35:*.gif=00;35:*.bmp=00;35:*.xbm=00;35:*.xpm=00;35:*.png=00;35:*.tif=00;35:"
export JAVA_HOME="$HOME/opt/OpenJDK/jdk"
export PATH="$HOME/opt/bin:$HOME/usr/bin:$HOME/.linux-env/usr/bin:$HOME/.local/bin:$PATH"
export PATH="$JAVA_HOME/bin:$PATH"
export PATH="$HOME/opt/Eclipse/eclipse:$PATH"
export PYTHONPATH="/home/edward/usr/tools/dev-tool/python"
export SVN_REPO="$HOME/Database/Repo/SVN"
export GIT_REPO="$HOME/Database/Repo/GIT"
export SVN_URL="file://$SVN_REPO"
export WS="$HOME/Workspace"
export MSYS_LOC="/c/Users/Public/DevKit/MSYS2-x64/"

export RDP_HD1609="1920x1043"
export RDP_HD1610="1920x1136"

## ------------------------------------------------------
#    Prompt setting
## ------------------------------------------------------
cdexpr='.*/\(.*/.*\)$'
cdcwd=`expr "$PWD" : "$cdexpr"`

if [ -n "`uname | grep 'MINGW\|MSYS'`" ]; then
    export USER=$USERNAME
    PS1="\[\e[1;31m\]\u@\h:<$cdcwd>\[\e[0m\] "
else
    PS1="\[\e[1;91m\]\u@\h:<$cdcwd>\[\e[0m\] "
fi

#PS1="\[\e[1;32m\]\u@\u\[\e[0m\]:\[\e[1;34m\]<$cdcwd>\[\e[0m\] "
#PS1="\[\e[1;32m\]\u@]u\[\e[0m\]:\[\e[1;34m\]$cdcwd\[\e[0m\]$ "

## ------------------------------------------------------
#    Job alias
## ------------------------------------------------------

## ------------------------------------------------------
#    User alias
## ------------------------------------------------------
if [ -n "`uname | grep 'MINGW\|MSYS'`" ]; then
    alias cd='function func { cd "$*"; echo $PWD; cdcwd=`expr "/$PWD" : "$cdexpr"`; PS1="\[\e[1;31m\]\u@\h:<$cdcwd>\[\e[0m\] "; }; func'
else
    alias cd='function func { cd "$*"; echo $PWD; cdcwd=`expr "/$PWD" : "$cdexpr"`; PS1="\[\e[1;91m\]\u@\h:<$cdcwd>\[\e[0m\] "; }; func'
fi

#alias cd='function func { cd "$*"; echo $PWD; cdcwd=`expr "/$PWD" : "$cdexpr"`; PS1="\[\e[1;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]<$cdcwd>\[\e[0m\] "; }; func'
#alias cd='function func { cd "$*"; echo $PWD; cdcwd=`expr "/$PWD" : "$cdexpr"`; PS1="\[\e[1;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]$cdcwd\[\e[0m\]$ "; }; func'
alias c='clear'
alias h='history'
alias ls='ls -F --color=always'
alias la='ls -aF'
alias ll='ls -lhF'
alias lla='ls -alhF'
alias rm='rm -i'
alias cvst="cvs st | grep -E 'Locally|Patch|Merged'"
alias du='du -h'
alias df='df -h'
alias ssh='ssh -X'
alias grep='grep --color=auto'
alias grepl='function func { grep --color=always $* | less -R; }; func'
alias egrep='egrep --color=auto'
alias mkpatch='diff -Naur'
#alias ct='ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .'
#alias cs='cscope -Rbq -f'
alias ct='ctags -R'
alias cs='cscope -Rbkq'
#alias ctags='/home/ASIC3/users/hhyeh/VIM_plugin/ctags-5.8/ctags'
#alias setdis='setenv DISPLAY'
alias svn_del="find -type d -name '.svn' | xargs rm -rf"
alias svn_diff='function func { svn diff --diff-cmd=svndiff $*; }; func'
alias svn_mdiff="svn st | grep '^M' | awk '{print "'$2'"}' | xargs -i svn diff --diff-cmd=svndiff {}"
alias svn_stu="svn st | grep '^?' | awk '{print "'$2'"}'"
alias svn_sta="svn st | grep '^A' | awk '{print "'$2'"}'"
alias svn_std="svn st | grep '^D' | awk '{print "'$2'"}'"
alias svn_stm="svn st | grep '^M' | awk '{print "'$2'"}'"
alias svn_stc="svn st | egrep '^C| C ' | awk '{print "'$2'"}'"
alias svn_stl="svn st | grep '^!' | awk '{print "'$2'"}'"
alias git_stm="git status -s . | grep '^ M' | awk '{print "'$2'"}'"
alias git_stmc="git status -s . | grep '^M ' | awk '{print "'$2'"}'"
alias git_stu="git status -s . | grep '^??' | awk '{print "'$2'"}'"
alias git_sta="git status -s . | grep '^A' | awk '{print "'$2'"}'"
alias git_del="find -type d -name '.git' | xargs rm -rf"
alias git_diff='function func { git difftool -t gvimdiff -y $*; }; func'
alias gd='gvim -d'
alias acalc='function func { awk "BEGIN{ print $* }"; }; func'
alias xterm='xterm -fg gray -bg black'
alias fp_cmp='function func { echo "if ($*) 1 else 0" | bc; }; func'
alias rand='echo $RANDOM'
alias fn='function func { find -name $*; }; func'
alias fn_full='function func { find `\pwd` -name $*; }; func'
alias showfile='function func { find `\pwd`/$* -type f; }; func'
alias showdir='function func { find `\pwd`/$* -maxdepth 0 -type d; }; func'
alias tree='function func { tree -C $*; }; func'
alias title='function func { echo -en "\033]0;$*\a"; }; func'
alias find_empty='find -name ".git" -prune -o -type d -empty -print'
alias add-cflags='function func { export CFLAGS="-I$* ${CFLAGS}"; }; func'
alias add-ldflags='function func { export LDFLAGS="-L$* -Wl,--rpath=$* ${LDFLAGS}"; }; func'
alias vim-swap='find ~/.vim/swap -name "%*" | xargs -i basename {} | sed "s/\%/\//g; s/\.swp$//g"'

## ------------------------------------------------------
#    Gnome alias
## ------------------------------------------------------
alias pc-suspend='systemctl suspend'
#alias pc-hibernate='systemctl hibernate'
alias open='xdg-open'
alias rdp-edward-nb-1610="xfreerdp /u:edward /size:$RDP_HD1610 /v:edward-nb /sound /microphone"
alias rdp-edward-nb-1609="xfreerdp /u:edward /size:$RDP_HD1609 /v:edward-nb /sound /microphone"
alias rdp-dell-da310-1610="xfreerdp /u:edward /size:$RDP_HD1610 /v:dell-da310 /sound /microphone"
alias rdp-dell-da310-1609="xfreerdp /u:edward /size:$RDP_HD1609 /v:dell-da310 /sound /microphone"
alias rdp-dell-da310-multi="xfreerdp /u:edward /v:dell-da310 /multimon /sound /microphone"

## ------------------------------------------------------
#    MINGW/MSYS Setting
## ------------------------------------------------------
if [ -n "`uname | grep 'MINGW\|MSYS'`" ]; then
    export PATH="$PATH:/c/Users/Public/DevKit/Vim/vim"
    alias gvim='/c/Windows/gvim.bat'
    alias gvimdiff='/c/Windows/gvimdiff.bat'
fi
