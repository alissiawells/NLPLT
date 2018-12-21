#!/usr/bin/env python3
import re
import os
import sys
import logging
import docx
from datetime import date
from typing import List, Any

import pymorphy2
import nltk

nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter

m = pymorphy2.MorphAnalyzer()
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from natasha import (
    DatesExtractor,
)

class Leviafunc(object):

    stopWords = set(line.strip() for line in open(os.path.abspath('files/RUstopwords.txt'), 'r'))
    countries = set(line.strip().lower() for line in open(os.path.abspath('files/countries.txt'), 'r'))
    organizations = set(line.strip().lower() for line in open(os.path.abspath('files/organizations.txt'), 'r'))

    def __init__(self, document, corp='corpus.txt', stopWords=stopWords, countries=countries, organizations=organizations, option="-c"):
        self.option = option
        self.stopWords = stopWords
        self.countries = countries
        self.organizations = organizations
        self.corpus = self.preprocess(self.getText(corp))
        self.doc_lines = self.getText(document)
        self.doc = self.preprocess(self.doc_lines)
        self.doc_tfidf = self.data_tfidf(self.data_tfidf(self.doc, " "), " ")
        self.corpus_tfidf = self.data_tfidf(self.data_tfidf(self.corpus, " ", space=" "), " ")

    def getText(self, document):
        try:
            if document.endswith(".txt"):
                with open(os.path.abspath('files/' + document), "r") as f:
                    return f.readlines()
            elif document.endswith(".docx"):
                doc = docx.Document(os.path.abspath('files/' + document))
                fullText = []
                for para in doc.paragraphs:
                    fullText.append(para.text)
                text = '\n'.join(fullText)
                file_lines = []
                for line in text.splitlines():
                    if line != '':
                        file_lines.append(line)
                return file_lines
            else:
                raise FileNotFoundError("Unsupported format of file")
        except IndexError:
            logging.error("Incorrect input")

    def lemm(self, word):
        word = re.sub('(</?.*?>)|(<>)|(\\d|\\W)+', '', word).lower()
        return m.parse(word)[0].normal_form.strip()

    def preprocess(self, doc_lines):
        return [[self.lemm(word) for word in word_tokenize(text) if ((self.lemm(word) not in self.stopWords) and len(word) > 3)]
                for text in doc_lines]

    def data_tfidf(self, text_lines, sep, space=""):
        data = ""  # type: str
        for line in text_lines:
            data += sep.join(line) + space
        return data

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(self, feature_names, sorted_items, topn=20):
        sorted_items = sorted_items[:topn]
        score_vals = []
        feature_vals = []
        for idx, score in sorted_items:
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]
        return results

    def count_tfidf(self, doc, corpus_tfidf):
        cv = CountVectorizer(max_df=0.85, stop_words=self.stopWords)
        word_count_vector = cv.fit_transform(word_tokenize(corpus_tfidf))
        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        tfidf_transformer.fit(word_count_vector)
        feature_names = cv.get_feature_names()

        tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))  # enumerates a vector of tf-idf scores
        sorted_items = self.sort_coo(tf_idf_vector.tocoo())
        return self.extract_topn_from_vector(feature_names, sorted_items, 20)

    def words_to_bigramms(self, text, str_bigrams=""):
        for line in text:
            bigrams = ngrams(line, 2)
            for k1, k2 in Counter(bigrams):
                str_bigrams += k1 + "_" + k2 + "_" + " "
        return str_bigrams

    def words_to_trigramms(self, text, str_trigrams=""):
        for line in text:
            trigrams = ngrams(line, 3)
            for k1, k2, k3 in Counter(trigrams):
                str_trigrams += k1 + "_" + k2 + "_" + k3 + " "
        return str_trigrams

    def title(self):
        logging.info('Extracting title')
        return self.doc_lines[0]

    def organizations_print(self):
        logging.info('Extracting organizations')
        orgs = []
        orgs_ = [[word for word in line if (word in self.organizations)] for line in self.doc]
        for line in orgs_:
            for word in line:
                orgs.append(word[0].upper() + word[1:])
        return list(set(orgs))

    def countries_print(self):
        logging.info('Extracting counties')
        coun = []
        coun_euristics = [[word for word in line if (word in self.countries)] for line in self.doc]
        for line in coun_euristics:
            for word in line:
                coun.append(word[0].upper() + word[1:])
        return list(set(coun))

    def typeofdoc(self):
        logging.info('Analyzing type of agreement')
        title = str(self.doc_lines[0]).strip()
        act_type = ["в рамках", "содружества", "государств-участников", "межгосударственном"]
        title_lemm = ' '.join([self.lemm(word) for word in word_tokenize(title)])
        for word in act_type:
            if self.lemm(word) in title_lemm:
                type = "Многостороннее соглашение"
            else:
                type = "Двустороннее соглашение"
        return type

    def area(self):
        logging.info('Analyzing area')
        title = str(self.doc_lines[0]).strip()
        topic = title.split(' ')[-2:]
        noun = m.parse(topic[1])[0]
        adj = m.parse(topic[0])[0].inflect({noun.tag.gender, 'sing', 'nomn'})
        return adj[0][0].upper() + adj[0][1:].lower() + " " + self.lemm(noun[0])

    def get_dates(self):
        logging.info('Extracting dates')
        extractor = DatesExtractor()
        res = []
        for line in self.doc_lines:
            matches = extractor(line)
            for index, match in enumerate(matches):
                try:
                    res.append(date(match.fact.year, match.fact.month, match.fact.day))
                except TypeError:
                    logging.error("\"Наташа\" не может распарсить дату в неполном формате %s %s %s" % (
                    match.fact.year, match.fact.month, match.fact.day))
        if len(res) > 1:
            dates = [res.pop(res.index(max(res))), max(res)]
            return dates
        elif len(res) == 1:
            logging.warning("В документе указана только одна дата")
            dates = [res[0], ""]
            return dates
        else:
            logging.warning("Даты не найдены")

    def keywords(self):
        logging.info('Extracting key words')
        kw = list(self.count_tfidf(self.doc_tfidf, self.corpus_tfidf))
        kw_euristics = [[word for word in line if (word[-3:] == "ция")] for line in self.doc]
        for line in kw_euristics:
            for word in line:
                kw.append(word)
        return list(set(kw))

    def keyphrases(self):
        logging.info('Extracting key phrases')
        kph = list(self.count_tfidf(self.words_to_bigramms(self.corpus), self.words_to_bigramms(self.doc)))
        kph += list(self.count_tfidf(self.words_to_trigramms(self.corpus), self.words_to_bigramms(self.doc)))
        return kph

    def status(self):
        logging.info('Analyzing status')
        if "" in self.get_dates():
            return "Не указана дата введения в действие"
        else:
            return "Статус: Введен в действие"

    def print_all(self):
        logging.info('Analyzing file')
        res = ["Название документа: " + self.title(),
               "Организации:"]
        res.extend(self.organizations_print())
        res.append("Страны:")
        res.extend(self.countries_print())
        res.append("Вид документа: " + self.typeofdoc())
        res.append("Направление: " + self.area())
        res.append("Область: " + self.area())
        dates = self.get_dates()
        if self.get_dates():
            res.append("Дата заключения: " + str(dates[0]))
            res.append("Дата вступления в силу: " + str(dates[1]))
        res.append("Ключевые слова:")
        res.extend(self.keywords())
        res.append("Наиболее часто встречающиеся выражения (n-gramms):")
        res.extend(self.keyphrases())
        res.append(self.status())
        return res

    def show_output(self, option):
        if option == "-f":
            with open(output, "w") as f:
                for i in self.print_all():
                    f.write(i+"\n")
        if option == "-c":
            for i in self.print_all():
                print(i)


if __name__ == "__main__":

    while True:

        if (len(sys.argv) > 3) and ("-c" in sys.argv):
            corp = os.path.abspath('files/'+sys.argv[sys.argv.index("-c") + 1])

        if len(sys.argv) == 3:
            if sys.argv[2] == "-f":
                output = os.path.abspath('files', 'output.txt')
            else:
                output = os.path.abspath('files/'+sys.argv[2])
            lev = Leviafunc(sys.argv[1], option="-f")
            lev.show_output("-f")
            break
        elif len(sys.argv) == 2:
            lev = Leviafunc(sys.argv[1])
            lev.show_output("-c")
            break
        else:
            print("Usage: python leviafunc.py input.txt [-f / output.txt] [-c corpus.txt]\n additional arguments: \
            \nfor console output add '-f' to write output in 'output.txt' \
              \nor type name of file for output instead '-f' \
              \nif you want to fit model on your own corpus, add '-c corpus.txt' \
              \nadd all files in directory \"file\" \nsupported formats of files: .txt, .docx")
