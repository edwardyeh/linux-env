#!/bin/csh -f
echo "Running .cshrc ..."
echo "Shell evnironment setting ..."

## ------------------------------------------------------
#    Common enviroment
## ------------------------------------------------------
set history=100    		# history list size
set savehist=100        # save history when logout
set autologout=0    	# disable autologout
set filec       		# file name matching
set notify      		# background jobs status notification
unset noclobber     	# disable output redirection to overwrite existing files
umask 022       		# file permission mask ; rwxr#xr#x
limit coredumpsize 0    # limit coredump size
set cdpath=(~)      	# easy convenient path search & change
set localdis= $DISPLAY
set pcdis= ""

if ($?VNCDESKTOP) then
setenv DISPLAY  $VNCDESKTOP":01"
endif

set path = (/bin /usr/bin /usr/etc /etc .)

if ( $?prompt ) then 
  stty erase "^H" kill "^U" intr "^C"  eof "^D" susp "^Z" echoe
endif

stty sane

########################################################
###        Edward Yeh's environment                  ###
########################################################
setenv LANG         "en_US.UTF-8"
setenv LS_COLORS    "no=00:fi=00:di=00;94:ln=00;36:pi=40;33:so=00;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:ex=00;32:*.cmd=00;32:*.exe=00;32:*.com=00;32:*.btm=00;32:*.bat=00;32:*.sh=00;32:*.csh=00;32:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.gz=00;31:*.bz2=00;31:*.bz=00;31:*.tz=00;31:*.rpm=00;31:*.cpio=00;31:*.jpg=00;35:*.gif=00;35:*.bmp=00;35:*.xbm=00;35:*.xpm=00;35:*.png=00;35:*.tif=00;35:"

## ------------------------------------------------------
#    Path & prompt setting
## ------------------------------------------------------
set cdexpr = '.*/\(.*/.*\)$'
set cdcwd  = `expr "/$cwd" : "$cdexpr"`
#set prompt = "`hostname`:<$cdcwd>[\!] "
#set prompt = "`hostname`> "
set prompt = "%{\033[1;31m%}`hostname`>%{\033[0m%} "

## ------------------------------------------------------
#    Job alias
## ------------------------------------------------------

## ------------------------------------------------------
#    User alias
## ------------------------------------------------------
alias cd            'set old=$cwd; chdir \!*; echo $cwd; set cdcwd=`expr "/$cwd" : "$cdexpr"`; set prompt="%{\033[1;31m%}`hostname`:<$cdcwd>%{\033[0m%} "'
alias back          'set back=$old; cd $back; unset back'
alias c             "clear"
alias h             "history"
alias ls            "ls -F \!* --color=always"
alias la            "ls -aF \!*"
alias ll            "ls -lhF \!*"
alias rm            "rm -i"
alias cvst          "cvs st | grep -E 'Locally|Patch|Merged'"
alias du            "du -h"
alias df            "df -h"
alias ssh 			"ssh -X"
alias grep			"grep --color=auto"
alias mkpatch		"diff -Naur"
#alias ct            "ctags -R --c++-kinds=+p --fields=+iaS --extra=+q ."
#alias cs            "cscope -Rbq -f"
alias ct            "ctags -R"
alias cs            "cscope -Rbkq"
#alias ctags         "/home/ASIC3/users/hhyeh/VIM_plugin/ctags-5.8/ctags"
alias setdis        "setenv DISPLAY"

## ------------------------------------------------------
#    GhostScript
## ------------------------------------------------------
setenv GS_LIB /usr/public/share/ghostscript/5.01:/usr/public/share/ghostscript/gsfonts:/usr/public/share/ghostscript/other_fonts

