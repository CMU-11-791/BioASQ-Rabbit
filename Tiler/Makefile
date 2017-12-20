IMAGE=deiis/tiler
NAME=tiler
PORT=8082

docker:
	docker build -t $(IMAGE) .
	
start:
	docker run -d -p $(PORT):8080 --name $(NAME) $(IMAGE)

test:
	curl -i -H 'Content-type:text/plain' -d '["Fried green tomatoes.", "Fried green apples."]' http://localhost:$(PORT)/concat

stop:
	docker rm -f $(NAME)
