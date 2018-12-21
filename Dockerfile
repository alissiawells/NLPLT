FROM python:3.6-slim

RUN apt-get update && apt-get install -y unixodbc-dev gcc g++

RUN pip install \ jupyter \ numpy \ scikit-learn==0.20.1 \ nltk==3.2.1 \ pymorphy2==0.8 \ dateparser==0.7.0 \ natasha==0.10.0 \ yargy==0.11.0 \ yake==0.3.7 \ python-docx==0.8.7

RUN python -m nltk.downloader punkt

RUN python -c 'example.py'

CMD mkdir src 

WORKDIR src
