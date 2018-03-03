REPO=docker.lappsgrid.org
NAME=base
IMAGE=bioasq-rabbit/$(NAME)
TAG=$(REPO)/$(IMAGE)
TGZ=deiis-rabbit.tgz

docker:
	#if [ ! -e $(TGZ) ] ; then cp ../deiis/$(TGZ) . ; fi
	docker build -t $(IMAGE) .

push:
	docker tag $(IMAGE) $(TAG)
	docker push $(TAG)

run:
	docker run -it --name $(NAME) $(IMAGE) /bin/bash

stop:
	docker rm -f $(NAME)

help:
	@echo
	@echo "GOALS"
	@echo
	@echo "docker - builds the image [default]"
	@echo "push   - pushes the image to $REPO"
	@echo "run    - runs the Docker container"
	@echo "stop   - stops a running Docker container"			
	@echo "help   - prints this help message"
	@echo
		