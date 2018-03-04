
.PHONY: deiis docker expander ranker results tiler

all: deiis docker expander ranker results tiler

help:
	@echo "GOALS"
	@echo
	@echo "deiis    - installs the deiis library"
	@echo "docker   - builds the base Docker image"
	@echo "expander - builds the container for the Expander"
	@echo "ranker   - builds the container for the Ranker"
	@echo "tiler    - builds the container for the Tiler"
	@echo "results  - builds the container for the Results service"
	@echo "rabbit   - starts the RabbitMQ container"
	@echo "help     - prints this help message"
	@echo

deiis:
	make -C deiis	

docker:
	make -C docker docker tag

expander:
	make -C Expander download docker
	
ranker:
	make -C Ranker
	
results:
	make -C Results
	
tiler:
	make -C Tiler

rabbit:
	docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management
