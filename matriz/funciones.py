import numpy as np
import re
import math

def extract_words(sentence):
    words = re.sub("[^\w]", " ",  sentence).split() 
    return words

def create_Vocabulary(words,dic_words):
	words = sorted(list(set(words)))
	for w in words:
		if(w in dic_words):
			dic_words[w] = dic_words[w]+1
		else:
			dic_words.setdefault(w,1)
	return dic_words

def tokenize_sentences(sentences):
	vocabulary = {}
	aux_vocabulary = {}
	file = open ("bagWords.txt","w")
	for sentence in sentences:
		aux_vocabulary = create_Vocabulary(sentence,aux_vocabulary)
	
	vocabulary.update(aux_vocabulary)
	file.write(str(vocabulary))
	file.close()
	return vocabulary

def list_dictionary(list_text):
	list_dico = [];
	for text in list_text:
		dictionary = {}
		for word in text:
			if(word not in dictionary):
				dictionary.setdefault(word,text.count(word))
		list_dico.append(dictionary)
	return list_dico

def showMatriz(vocabulary,list_dictionary):
	file = open("resultado.txt","w")
	matriz = []
	print("Palabra\tD1\tD2\tD3")
	print("")
	for word in vocabulary:
		print(word,end=" ")
		for dico in list_dictionary:
			if(word not in dico):
				print ("\t 0",end=" ")
			else:
				print("\t "+str(dico[word]),end=" ")
		print()
	file.close()

# Medicion de la similitud
"""
def euclidean_distance(vector1,vector2):
	distance = 0
	for i in range(len(vector1)):
		distance += (vector2[i]-vector1[i])**2
	return math.sqrt(distance)
"""
def create_list(vocabulary,dictionary):
	data = []
	for word in vocabulary:
		if(word in dictionary):
			data.append(dictionary[word])
		else:
			data.append(0)
	return data

def cosine_similarity(vector1,vector2):
	vectorA = np.array(vector1)
	vectorB = np.array(vector2)
	cosine = (np.dot(vector1,vector2))/((math.sqrt(np.dot(vector1,vector1))) * np.sqrt((np.dot(vector2,vector2))))
	return cosine