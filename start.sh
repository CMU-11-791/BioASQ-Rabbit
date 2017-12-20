#!/usr/bin/env bash

for dir in Expander Ranker Tiler Results; do
	echo "Starting $dir"
	cd $dir
	python service.py &
	cd -
done 
echo "Services started"