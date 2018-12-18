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

use jupyter notebook (Analysis_of_testdoc.ipynb) or the module:
```sh
pip install leviafunc
```
Usage:
```sh
import leviafunc
doc = leviafunc.analyse("document.txt") # .doc, .docx are also supported
doc.print_all() # output: all fields 
doc.title() # or print them partly
doc.organizations()
doc.countries()
doc.type()
doc.area()
doc.dates()
doc.keywords()
doc.keyphrases()
```

![](https://github.com/alissiawells/Leviafunc/blob/master/Leviathan.jpg)
