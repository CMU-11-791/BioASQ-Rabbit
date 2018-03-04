FROM docker.lappsgrid.org/bioasq-rabbit/base

COPY *.py /root/
COPY logging.ini /root
WORKDIR /root
#RUN python -c "import nltk; nltk.download('stopwords')"
ENTRYPOINT ["python", "service.py"]
