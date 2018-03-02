FROM docker.lappsgrid.org/deiis/base

COPY *.py /root/
COPY logging.ini /root

ADD https://downloads.lappsgrid.org/deiis-rabbit.tgz /root/deiis
RUN cd /root/deiis && python setup.py install
WORKDIR /root
ENTRYPOINT ["python", "service.py"]
