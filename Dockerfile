FROM python:3.6-slim

RUN apt-get update && apt-get install -y unixodbc-dev gcc g++

RUN pip install torch==0.4.1 RUN pip install flair==0.3.2

RUN pip install \ pymorphy2==0.8 \ jupyter \ nltk==3.2.1 \ gensim==2.1.0 \ scikit-learn==0.20.1 \ dateparser==0.7.0 \ natasha==0.10.0 \ yargy==0.11.0 \ yake==0.3.7 \ python==docx-0.8.7

RUN python -m nltk.downloader stopwords && python -m nltk.downloader punkt && \ python -m nltk.downloader averaged_perceptron_tagger

RUN python -c 'import flair; _ = flair.models.SequenceTagger.load("ner-fast")'

CMD mkdir src 

WORKDIR src
