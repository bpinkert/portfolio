#!/bin/bash
#
# Debian/Ubuntu installation script for PIL
#

sudo apt-get install -y python-dev python-setuptools python3-dev python3-setuptools

sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk


sudo pip install Pillow
