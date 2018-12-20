import leviafunc as lf

# for the most of use cases it is enough to define only document
#lev = lf.Leviafunc('testdoc.txt') # input type: str ; check if the file is in the same directory or define the path

# all outputs in a file
#lev = lf.Leviafunc(document, option="-f")
#lev.show_output("-f")

# optional argument to fit model on another corpus
#lev = lf.Leviafunc('input.txt', corp='yourcorpus.txt')

#lev = lf.Leviafunc('testdoc.txt', '/home/user/Leviafunc/corpus.txt')

print(lev.title()) # output type: str
for org in lev.organizations_print(): # output type: list of str
    print(org)
coun = lev.countries_print() # output type: list of str
print(coun)
print(lev.typeofdoc()) # output type: str
print(lev.area()) # output type: str
dates = lev.get_dates() # output type: sorted list of 'datetime.date' objects
print("Дата заключения:" + str(dates[0]))
print("Дата вступления в силу:" + str(dates[1]))
keywords = lev.keywords() # output type: list of str
ngramms = lev.keyphrases() # output type: list of str
for i in keyword.extend(ngramms):
    print(i)
# i'm not sure the status of a legal act is a question of NLP but the customer asked me to implement this :(
lev.status()


