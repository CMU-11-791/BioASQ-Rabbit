FROM deiis/base-image

COPY *.py /root/
COPY logging.ini /root

WORKDIR /root
ENTRYPOINT ["python", "service.py"]
