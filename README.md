```sh
Leviafunc(legal_acts):
    return work_of_Leviathan
```
# NLP of legal texts
Analysis of agreements between governments

* Key words & key phrases extraction with TF-IDF and N-gramms
* NER for DATES with (Natasha (rule-based lib for Russian language). 
Sequence model, implemented in AnaGo and NER by DeepMIPT both have lower accuracy for this type of documents.
* Dictionary method with morphological analysis for finding ORGANIZATIONS and COUNTRIES 

### Use as a module:
or run:
```sh
$ pip install leviafunc
$ python
$ import leviafunc as lf
$ lev = lf.Leviafunc('testdoc.txt')
$ print(lev.keywords())
$ print(lev.keyphrases())
```
more use cases are described in example.py

### Run as a script:
```sh
$ python leviafunc.py input.txt [-f / output.txt] [-c corpus.txt]
```
or run without additional options for console output and initial corpus for training the model

### Analyze texts with jupyter notebook:
```sh
git clone https://github.com/alissiawells/Leviafunc.git
$ cd Leviafunc
$ mkvirtualenv Leviafunc
$ pip install -r requirements.txt
$ jupyter notebook
```
then open in browser 'Analysis.ipynb'

or use Docker


![](https://github.com/alissiawells/Leviafunc/blob/master/Leviathan.jpg)
