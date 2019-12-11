import simplejson
import re


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

titles = []
json_file = open('PoPAlcoholismComorbidity.json')
popDocuments = simplejson.load(json_file)
for paper in popDocuments:
    for attribute, value in paper.iteritems():
        if attribute == "title":
            titles.append(value)




stopwords = [line.rstrip('\n') for line in open("EnglishStopWords.txt")]


wordList = []
for i in titles:
    wordList.extend(re.sub("[^\w]", " ",  i).split())

wordList = list( dict.fromkeys(wordList) ) #trick to remove duplicates



wordfreq = [wordList.count(p) for p in wordList]
wordfreq =  dict(zip(wordList,wordfreq))

wordfreq= sortFreqDict(wordfreq)

for i in wordfreq:
    print i
