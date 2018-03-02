NAME=expander
IMAGE=deiis/$(NAME)

META=http://downloads.lappsgrid.org/deiis/metamap.tgz
PY=http://downloads.lappsgrid.org/deiis/pymetamap.tgz

docker:
	docker build -t $(IMAGE) .
	
download:
	if [ ! -x $(META) ] ; then wget $(META) ; fi
	if [ ! -x $(PY) ] ; then wget $(PY) ; fi

start:
	docker run -d -p $(PORT):8080 --name $(NAME) $(IMAGE)

stop:
	docker rm -f $(NAME)
