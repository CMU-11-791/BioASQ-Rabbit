#!/usr/bin/env bash

docker rm $(docker ps -q -f "status=exited")