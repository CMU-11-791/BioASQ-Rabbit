FROM docker.lappsgrid.org/bioasq-rabbit/base

COPY *.py /root/
COPY logging.ini /root

WORKDIR /root
ENTRYPOINT ["python", "service.py"]
