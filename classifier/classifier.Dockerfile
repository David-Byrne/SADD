FROM python:3.6.4
COPY secrets.json /
COPY classifier/ /classifier
WORKDIR /classifier
EXPOSE 8000
RUN pip install -r classifier.requirements.txt
RUN python -m nltk.downloader stopwords twitter_samples
RUN python model_generator.py
CMD ["gunicorn", "--bind=0.0.0.0:8000", "-w=4", "server:app"]
