FROM python:3.6.4
COPY secrets.json /
COPY analyser/ /analyser
WORKDIR /analyser
RUN pip install -r analyser.requirements.txt
RUN python -m nltk.downloader webtext
CMD ["python", "-u", "analyser.py"]
