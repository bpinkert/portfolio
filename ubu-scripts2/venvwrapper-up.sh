#!/bin/bash
#
# script to install virtualenv wrapper, create the directories and the source the new .bashrc file
#
sudo pip install virtualenvwrapper
mkdir ~/.virtualenvs
mkdir ~/Devel

echo ' ' >> ~/.bashrc
echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bashrc
echo 'export PROJECT_HOME=$HOME/Devel' >> ~/.bashrc
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
source ~/.bashrc
