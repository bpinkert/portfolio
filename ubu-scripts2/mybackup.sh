#!/bin/bash
# Description: backs up a directory and sends it to remote machine in specified directory
#
# Params
# $1: directory to backup
# $2: remote username
# $3: remote ip address or host
# $4: destination to store backup

x=$(date +"%Y%m%d")
y=$(date +"%H%M%S")

#tar the directory
tar -cvz -f mybackup.tz $1
cp mybackup.tz backup-$x-$y.tz
file=$(pwd)/backup-$x-$y.tz
scp $file $2@$3:/$4
rm backup-$x-$y.tz
rm mybackup.tz

