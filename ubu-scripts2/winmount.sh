#!/bin/bash
# Description: mounts windows directory, accepts input with 4 params
# and asks for password within console. if mount point doesn't exist
# then it creates it with sudo privs
#
# Params
# $perms: read/write or read-only
# $1: remote username
# $2: remote machine ip address
# $3: remote folder
# $4: local mountpoint

echo -e "Enter ro for read-only or rw for read-write"
echo -e "Blank is read-only:"
read perms
# if perms is empty then set to ro
while [ -z "$perms" ]
do
$perms="ro"
# mount and accept commandline parameters
if [ ! -d "$4" ]; then
	mount -t cifs -o $perms,username=$1 //$2/$3 $4
else
	sudo mkdir -p $4
	mount -t cifs -o $perms,username=$1 //$2/$3 $4
