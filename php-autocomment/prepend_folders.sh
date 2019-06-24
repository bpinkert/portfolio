#!/bin/bash
for D in `find . -type d`
do
    `python prepend.py -d $D`
done


for D in 2017-04-[01-20]
do
	echo $D
done