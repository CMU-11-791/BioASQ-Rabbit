FROM docker.lappsgrid.org/bioasq-rabbit/base

ADD metamap.tgz /usr/local/share
WORKDIR /usr/local/share/public_mm/bin
RUN echo "/usr/local/share/public_mm" | ./install.sh

ADD pymetamap.tgz /root
WORKDIR /root/pymetamap
RUN python setup.py install


WORKDIR /root
COPY *.py /root/
COPY *.ini /root/

ENTRYPOINT ["python", "service.py"]
