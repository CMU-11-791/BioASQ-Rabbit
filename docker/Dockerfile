# Base image for all other images generated for this project. The base image
# includes Python and all required Python packages (Flask, NLTK, etc).

FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python-pip python-dev python-numpy \
    python-scipy python-matplotlib git subversion emacs24-nox ant \
    libblas-dev liblapack-dev libatlas-base-dev gfortran libxml2-dev \
    libxslt1-dev zlib1g-dev

RUN apt-get install -y openjdk-8-jdk

# Fixes problem grabbing Grapes in Groovy/LSD scripts.  Not sure if this (or
# equivalent) is needed on RedHat/CentOS.
# See: https://github.com/lappsgrid-incubator/galaxy-appliance/issues/4
RUN /var/lib/dpkg/info/ca-certificates-java.postinst configure

COPY requirements.txt /root

WORKDIR /root
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

#COPY logging.ini /root
ADD deiis-rabbit.tgz /root/deiis
RUN cd /root/deiis && python setup.py install

