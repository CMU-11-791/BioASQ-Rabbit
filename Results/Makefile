NAME=results

include ../Makefile.master

ifndef RABBIT_HOST
start:
	@echo "Please export RABBIT_HOST before staring the Docker container."
else
start:
	docker run -it -v /tmp:/tmp -e RABBIT_HOST=$(RABBIT_HOST) --name $(NAME) $(IMAGE) /bin/bash
endif
