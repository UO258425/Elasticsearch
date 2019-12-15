import simplejson
import re
from langdetect import detect

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def printList(aList):
    for i in aList:
        print(i)


#First we collect just the titles of the pop documents
titles = []
json_file = open('pop.json')
popDocuments = simplejson.load(json_file)
for paper in popDocuments:
    for attribute, value in paper.items():
        if attribute == "title":
            titles.append(value)

#printList(titles)

#Now we remove all titles that are not written in english
#Langdetect is not perfect and non deterministic, so sometimes values changes at
# different executions.
for title in titles:
    if detect(title) != 'en':
        titles.remove(title)
#printList(titles)

#We remove all english stopwords from the titles
stopwords = [line.rstrip('\n') for line in open("EnglishStopWords.txt")]

#Then we convert it to a list of words, and we remove duplicates
wordList = []
for i in titles:
    wordList.extend(re.sub("[^\w]", " ",  i).split())

#printList(wordList)

wordfreq = [wordList.count(p) for p in wordList]
wordfreq =  dict(zip(wordList,wordfreq))

wordfreq= sortFreqDict(wordfreq)

mostRelevantPoPWords = list()

for entry in wordfreq:
    try:
        if entry[0] >= 10 and not (entry[0].isdigit()):
            mostRelevantPoPWords.append(entry[1].lower())
    except:
        pass


mostRelevantPoPWords = list( dict.fromkeys(wordList) ) #trick to remove duplicates
for stopword in stopwords:
    if stopword in mostRelevantPoPWords:
        mostRelevantPoPWords.remove(stopword)



outputFile = open("popOutput.txt", "wt")
outputFile.write("\n".join(mostRelevantPoPWords))
