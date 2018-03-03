define del
	if [ -d $(1) ] ; then rm -rf $(1) ; fi
endef

install:
	python setup.py install
	tar czf deiis-rabbit.tgz README.md setup.py setup.cfg deiis/
	if [ -e ~/.ssh/lappsgrid-shared-key.pem ] ; then scp -i ~/.ssh/lappsgrid-shared-key.pem deiis-rabbit.tgz root@downloads.lappsgrid.org:/var/lib/downloads/deiis ; fi
	cp deiis-rabbit.tgz ../docker
	
clean:
	$(call del,build)
	$(call del,deiis.egg-info)
	$(call del,dist)
	rm *.tgz
