#!/usr/bin/env bash
while [ -n "$1" ] ; do
	ps | grep $1 | grep python | awk '{print $1}' | xargs kill
	shift
done
	