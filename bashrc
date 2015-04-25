#!/bin/bash -f
echo "Running .bashrc ..."
echo "Shell evnironment setting ..."
echo ""

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

## ------------------------------------------------------
#    Common enviroment
## ------------------------------------------------------
umask 022       		# file permission mask ; rwxr#xr#x
export TMOUT=3600       # disable auto-logout

HISTSIZE=100    		# history list size
HISTFILESIZE=100        # save history when logout
localdis=$DISPLAY
pcdis=""

stty erase "^H" kill "^U" intr "^C"  eof "^D" susp "^Z" echoe
stty sane

########################################################
###        Edward Yeh's environment                  ###
########################################################
export  LANG="en_US.UTF-8"
export  LS_COLORS="no=00:fi=00:di=00;94:ln=00;36:pi=40;33:so=00;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:ex=00;32:*.cmd=00;32:*.exe=00;32:*.com=00;32:*.btm=00;32:*.bat=00;32:*.sh=00;32:*.csh=00;32:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.gz=00;31:*.bz2=00;31:*.bz=00;31:*.tz=00;31:*.rpm=00;31:*.cpio=00;31:*.jpg=00;35:*.gif=00;35:*.bmp=00;35:*.xbm=00;35:*.xpm=00;35:*.png=00;35:*.tif=00;35:"
export  PATH+=":$HOME/.linux-env/usr/bin"
export  SVN_DB="$HOME/Datebase/SVN_DB"
export  SVN_PATH="file://$SVN_DB"
export  GIT_DB="$HOME/Database/GIT_DB"

if [ -z $LD_LIBRARY_PATH ]; then
    export LD_LIBRARY_PATH="/usr/local/lib"
else
    export LD_LIBRARY_PATH+=":/usr/local/lib"
fi

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
alias cd='function func { cd $*; echo $PWD; cdcwd=`expr "/$PWD" : "$cdexpr"`; PS1="\[\e[1;31m\]$HOSTNAME:<$cdcwd>\[\e[0m\] "; }; func'
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
alias mkpatch='diff -Naur'
#alias ct='ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .'
#alias cs='cscope -Rbq -f'
alias ct='ctags -R'
alias cs='cscope -Rbkq'
#alias ctags='/home/ASIC3/users/hhyeh/VIM_plugin/ctags-5.8/ctags'
alias setdis='setenv DISPLAY'
alias svn_del="find -type d -name '.svn' | xargs rm -rf"
alias svn_diff='function func { svn diff --diff-cmd=svndiff $*; }; func'
alias git_del="find -type d -name '.git' | xargs rm -rf"
alias git_diff='function func { git difftool -t gvimdiff -y $*; }; func'
alias gd='gvim -d'
alias acalc='function func { awk "BEGIN{ print $* }"; }; func'

## ------------------------------------------------------
#    GhostScript
## ------------------------------------------------------
#setenv GS_LIB /usr/public/share/ghostscript/5.01:/usr/public/share/ghostscript/gsfonts:/usr/public/share/ghostscript/other_fonts

