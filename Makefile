
.PHONY: deiis docker expander ranker results tiler

all: deiis docker expander ranker results tiler

help:
	@echo "GOALS"
	@echo
	@echo "deiis  - installs the deiis library"
	@echo "docker - builds the base Docker image"
	@echo "help   - prints this help message"
	@echo

deiis:
	make -C deiis	

docker:
	make -C docker docker push

expander:
	make -C Expander
	
ranker:
	make -C Ranker
	
results:
	make -C Results
	
tiler:
	make -C Tiler
