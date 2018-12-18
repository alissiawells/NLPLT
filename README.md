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

### Analyze texts with jupyter notebook:
```sh
git clone https://github.com/alissiawells/Leviafunc.git
$ cd Leviafunc
$ mkvirtualenv Leviafunc
$ pip install -r requirements.txt
$ jupyter notebook
```
then open in browser 'Analysis.ipynb' 


![](https://github.com/alissiawells/Leviafunc/blob/master/Leviathan.jpg)
