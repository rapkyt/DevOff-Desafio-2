#!/usr/bin/env bash

# =====================================
# BASHRC
# =====================================
# ~/.bashrc: executed by bash(1) for non-login shells.

# -------------------------------------
# Prompt
# -------------------------------------

set_prompts() {
    local black=""
    local blue=""
    local bold=""
    local cyan=""
    local green=""
    local orange=""
    local purple=""
    local red=""
    local reset=""
    local white=""
    local yellow=""

    local userStyle=""

    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        tput sgr0 # reset colors

        bold=$(tput bold)
        reset=$(tput sgr0)

        black=$(tput setaf 0)
        red=$(tput setaf 1)
        green=$(tput setaf 2)
        yellow=$(tput setaf 3)
        blue=$(tput setaf 4)
        purple=$(tput setaf 5)
        cyan=$(tput setaf 6)
        white=$(tput setaf 7)
    else
        bold=""
        reset="\e[0m"

        black="\e[1;30m"
        blue="\e[1;34m"
        cyan="\e[1;36m"
        green="\e[1;32m"
        purple="\e[1;35m"
        red="\e[1;31m"
        white="\e[1;37m"
        yellow="\e[1;33m"
    fi

    # build the prompt

    # logged in as root
    if [[ "$USER" == "root" ]]; then
        userStyle="\[$bold$red\]"
    else
        userStyle="\[$purple\]"
    fi

    # set the terminal title to the current working directory
    PS1="\[\033]0;\w\007\]"

    PS1+="\[$userStyle\]\u" # username
    PS1+="\[$reset$white\]: "
    PS1+="\[$white\] \w" # working directory
    PS1+="\n"
    PS1+="\[$reset$white\]\$ \[$reset\]" # $ (and reset color)
    export PS1
}

set_prompts
unset set_prompts

# -------------------------------------
# Aliases
# -------------------------------------

# You may uncomment the following lines if you want `ls' to be colorized:
export LS_OPTIONS='--color=auto'
eval "$(dircolors)"
alias ls='ls $LS_OPTIONS'
alias ll='ls $LS_OPTIONS -l'
alias l='ls $LS_OPTIONS -lA'

# Some more alias to avoid making mistakes:
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
