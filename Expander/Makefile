REPO=docker.lappsgrid.org
NAME=expander
IMAGE=bioasq-rabbit/$(NAME)
TAG=$(REPO)/$(IMAGE)

META=http://downloads.lappsgrid.org/deiis/metamap.tgz
PY=http://downloads.lappsgrid.org/deiis/pymetamap.tgz

docker:
	docker build -t $(IMAGE) .
	
download:
	if [ ! -x $(META) ] ; then wget $(META) ; fi
	if [ ! -x $(PY) ] ; then wget $(PY) ; fi

start:
ifndef RABBIT_HOST
	@echo "Using localhost as RABBIT_HOST"
	@echo "Please export RABBIT_HOST to use a different server."
	RABBIT_HOST=localhost
endif
	docker run -d -p $(PORT):8080 -e RABBIT_PORT=$(RABBIT_PORT) --name $(NAME) $(IMAGE)

stop:
	docker rm -f $(NAME)

push:
	docker tag $(IMAGE) $(TAG)
	docker push $(TAG)
	