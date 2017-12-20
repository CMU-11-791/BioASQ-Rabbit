IMAGE=deiis/ranker
NAME=ranker
PORT=8084

docker:
	docker build -t $(IMAGE) .
	
start:
	docker run -d -p $(PORT):8080 --name $(NAME) $(IMAGE)

#test:
#	curl -i -H 'Content-type:text/plain' -d "Fried green tomatoes." http://localhost:$(PORT)/similarity/jaccard

stop:
	docker rm -f $(NAME)
