import nltk
from nltk.book import *

#1 
print ('---1---')
print ( 12 / (4+1))

#2
print ('---2---')
print (26 ** 3)

#3
print ('---3---')
print (['monthy','Python'] * 20)
print (3 * sent1)
#4
print ('---4---')
print ("Words: ",len(text2))
print("Distinct words:", len(set(text2)))
#6
print ('---6---')
text2.dispersion_plot(['Elinor', 'Marianne', 'Edward', 'Willoughby'])
#7
print ('---7---')
text5.collocations()

#9
print ('---9---')
my_string = 'Ejercicio 9'
print (my_string)
print(my_string + my_string)
print(my_string * 3)

#10
print ('---10---')
my_sent = ['let', 'it', 'go', 'frozen', 'one', 'two']
sentence = ' '.join(my_sent)                             
print(sentence)
print(sentence.split())

#11
print ('---11---')
phrase1 = 'hello'
phrase2 = 'world'
print(len(phrase1 + phrase2))                  
print(len(phrase1) + len(phrase2))

#13
print ('---13---')
print (sent1[2][2])

#14
print ('---14---')

indices = [i for i, x in enumerate(sent3) if x == 'the']
print(indices)

#15
print ('---15---')
print(sorted(b for b in set(text5) if b.startswith('b')))

#16
print ('---16---')
print(list(range(10)))
print(list(range(10, 20)))
print(list(range(10, 20, 2)))
print(list(range(20, 10, -2)))

#17
print ('---17---')
print(text9.index('sunset'))
print(' '.join(text9[621:644]))

#18
print ('---18---')
print(len(sorted(set(sent1 + sent2 + sent3 + sent4 + sent5 + sent6 + sent7 + sent8))))

#19
print ('---19---')
print("1.- ", len(sorted(set(w.lower() for w in text1))))
print("2.- ", len(sorted(w.lower() for w in set(text1))))

#21
print ('---21---')
print(text2[-2:])

#22
print ('---22---')
fdist = FreqDist(w for w in text5 if len(w) == 4) 
print(fdist.most_common())

#23
print ('---23---')
words = [w for w in text6 if w.isupper()]
for w in words:
    print(w)

#24
print ('---24---')
a = [w for w in text6 if w.endswith('ize')]
b = [w for w in text6 if 'z' in w]
c = [w for w in text6 if 'pt' in w]
d = [w for w in text6 if w.istitle()]

print(a)
print(b)
print(c)
print(d)

#25
print ('---25---')
sent = ['she', 'sells', 'sea', 'shells', 'by', 'the', 'sea', 'shore']
print([w for w in sent if w.startswith('sh')])
print([w for w in sent if len(w) > 4])

#26
print ('---26---')
total_length = sum(len(w) for w in text1)
total_words = len(text1)
average = total_length / total_words
print (average)

#27
print ('---27---')
def vocab_size(text):
    return len(set(text))

#28
print ('---28---')
def percent(word, text):
    return 100 * text.count(word) / len(text)

#29
print('---29---')
print(set(sent3) < set(text1))