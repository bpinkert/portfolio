#!/bin/bash
#
#  Install script for basic ubuntu programs
#

sudo apt-get --assume-yes update
sudo apt-get --assume-yes upgrade

sudo apt-get install -y synaptic aptitude

cd ~/Downloads

wget http://c758482.r82.cf2.rackcdn.com/sublime-text_build-3083_amd64.deb

sudo dpkg -i sublime-text_build-3083_amd64.deb

sudo apt-get install -y git

sudo apt-get install -y openvpn

sudo apt-get install -y xclip

sudo apt-get install -y curl
