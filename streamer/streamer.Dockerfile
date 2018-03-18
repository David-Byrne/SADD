FROM python:3.6.4
COPY secrets.json /
COPY config.json /
COPY streamer/ /streamer
WORKDIR /streamer
RUN pip install -r streamer.requirements.txt
CMD ["python", "-u", "streamer.py"]
