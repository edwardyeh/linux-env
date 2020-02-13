#!/bin/bash -f
#echo "Running .bashrc ..."
#echo "Shell evnironment setting ..."
#echo ""

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

if [ -f ~/.bashrc_org ]; then
    source ~/.bashrc_org
fi

## ------------------------------------------------------
#    Common enviroment
## ------------------------------------------------------
umask 022               # file permission mask ; rwxr#xr#x
#export TMOUT=3600       # disable auto-logout
export TMOUT=0          # disable auto-logout

HISTSIZE=100            # history list size
HISTFILESIZE=100        # save history when logout
localdis=$DISPLAY
pcdis=""

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
export  TERM="xterm-256color"
export  LANG="en_US.UTF-8"
export  LC_ALL="en_US.UTF-8"
export  LS_COLORS="no=00:fi=00:di=00;94:ln=00;36:pi=40;33:so=00;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:ex=00;32:*.cmd=00;32:*.exe=00;32:*.com=00;32:*.btm=00;32:*.bat=00;32:*.sh=00;32:*.csh=00;32:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.gz=00;31:*.bz2=00;31:*.bz=00;31:*.tz=00;31:*.rpm=00;31:*.cpio=00;31:*.jpg=00;35:*.gif=00;35:*.bmp=00;35:*.xbm=00;35:*.xpm=00;35:*.png=00;35:*.tif=00;35:"
export  PATH="$HOME/opt/Eclipse/eclipse:$PATH"
export  PATH="$HOME/opt/OpenJDK/jdk/bin:$PATH"
export  PATH="$HOME/usr/bin:$HOME/.linux-env/usr/bin:$HOME/.linux-env/usr/bin/python:$PATH"
export  SVN_REPO="$HOME/Database/Repo/SVN"
export  GIT_REPO="$HOME/Database/Repo/GIT"
export  SVN_URL="file://$SVN_REPO"
export  WS="$HOME/Workspace"
export  MSYS_LOC="/c/Users/Public/DevKit/MSYS2-x64/"

## ------------------------------------------------------
#    Prompt setting
## ------------------------------------------------------
cdexpr='.*/\(.*/.*\)$'
cdcwd=`expr "$PWD" : "$cdexpr"`
#PS1="`hostname`:<$cdcwd>[\!] "
#PS1="`hostname`> "
PS1="\[\e[1;31m\]$HOSTNAME:<$cdcwd>\[\e[0m\] "

## ------------------------------------------------------
#    Job alias
## ------------------------------------------------------

## ------------------------------------------------------
#    User alias
## ------------------------------------------------------
alias cd='function func { cd "$*"; echo $PWD; cdcwd=`expr "/$PWD" : "$cdexpr"`; PS1="\[\e[1;31m\]$HOSTNAME:<$cdcwd>\[\e[0m\] "; }; func'
alias c='clear'
alias h='history'
alias ls='function func { ls -F $* --color=always; }; func'
alias la='function func { ls -aF  $*; }; func'
alias ll='function func { ls -lhF $*; }; func'
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

if [ -n "`uname | grep 'MINGW\|MSYS'`" ]; then
    export PATH="$PATH:/c/Users/Public/DevKit/Vim/vim81"
    alias gvim='/c/Windows/gvim.bat'
    alias gvimdiff='/c/Windows/gvimdiff.bat'
fi
