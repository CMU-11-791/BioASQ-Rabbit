#!/usr/bin/env bash

if [[ -z "$1" || "$1" = "python" ]] ; then
    for dir in Expander Ranker Tiler Results; do
        echo "Starting service $dir"
        cd $dir
        python service.py localhost &
        cd -
    done
    echo "Services started"
elif [[ "$1" = "docker" ]] ; then
    if [[ -z "$RABBIT_HOST" ]] ; then
        echo "Please export RABBIT_HOST and run this script again."
        exit 1
    fi
    for image in expander ranker tiler; do
        echo "Starting image $image"
        docker run -d --name $image -e RABBIT_HOST=$RABBIT_HOST bioasq-rabbit/$image
    done
    docker run -d --name results -v /tmp:/tmp -e RABBIT_HOST=$RABBIT_HOST bioasq-rabbit/results
else
    echo "Invalid option $1"
    exit 1
fi