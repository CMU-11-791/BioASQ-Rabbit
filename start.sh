#!/usr/bin/env bash

if [[ -z "$1" || "$1" = "python" ]] ; then
    for dir in Expander Ranker Tiler Results; do
        echo "Starting service $dir"
        cd $dir
        python service.py &
        cd -
    done
    echo "Services started"
elif [[ "$1" = "docker" ]] ; then
    for image in expander ranker tiler; do
        echo "Starting image $image"
        docker run -d --name $image -e RABBIT_HOST=$RABBIT_HOST bioasq-rabbit/$image
    done
    docker run -d --name results -v /tmp:/tmp -e RABBIT_HOST=$RABBIT_HOST bioasq-rabbit/results
else
    echo "Invalid option $1"
    exit 1
fi