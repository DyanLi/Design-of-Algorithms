#coding=utf-8
'''
use re to
caul the num of the words
alice=ALICE

change:
use these function
1,with open(...) as f:
2,content = f.read()
3,allwords = finditer( ... content ... ) 
  finditer is iter, findall is list
4,all_lower_words = imap(str.lower, allwords)
5,count = Counter(all_lower_words)
  much butter than build a empty dict
'''
import re,math
import itertools
import collections
from operator import itemgetter


with open('alice.txt',"rt")  as f:
    content=f.read()

allwords=re.findall(r'[a-zA-Z]+',content)
#if i use find finditer ,i cannot use imap,allwords is a list
all_lower_words = itertools.imap(str.lower, allwords)
count = collections.Counter(all_lower_words)


#dict sort method 1: change key and value
#cntSorted=dict((v,k) for k,v in cnt.iteritems())
#cntSorted.sort()
#important and not be neglected
#print list(cntSorted.iteritems())[-10:] 

#dict sort method 2: use lambda
#cntSorted=sorted(count.iteritems(),key=lambda d:d[1],reverse=True)
#print cntSorted[0:10]

#dict sort method 3: use operator
cntSorted=sorted(count.iteritems(),key=itemgetter(1),reverse=True)
print cntSorted[0:10]



#draw a pic
import matplotlib.pyplot as plt

#plt.bar(range(20), [cntSorted[i][1] for i in range(20)])
#plt.xticks(range(20), [cntSorted[i][0] for i in range(20)],rotation=30)

length=len(cntSorted)
plt.plot(range(length), [math.log(cntSorted[i][1],10) for i in range(length)])
plt.title(u"WordFrequencyAnalysis-zipf")
plt.show()