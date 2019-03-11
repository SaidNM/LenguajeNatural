import numpy as np
import re
import math

def extract_words(sentence):
    words = re.sub("[^\w]", " ",  sentence).split()
    words_cleaned = [w.lower() for w in words]
    return words_cleaned

def tokenize_sentences(sentences):
	words=[]
	file = open ("bagWords.txt","w")
	for sentence in sentences:
		aux_words = extract_words(sentence)
		words.extend(aux_words)

	words=sorted(list(set(words)))
	file.write(str(words))
	file.close()
	return words

def matrizTF(bag,datos):
	mTF = [];
	for dato in datos:
		v = vectorTF(bag,dato)
		mTF.append(v)
	return mTF

def vectorTF(bag,vector):
	vTF = []
	for word in bag:
		x = vector.count(word)
		vTF.append(x)
	return vTF

def showMatriz(bag,matriz):
	file = open("resultado.txt","w")
	b = np.array([bag,matriz[0],matriz[1]])
	file.write(str(np.transpose(b)))
	print(np.transpose(b))
	file.close()
# Medicion de la similitud
"""
def euclidean_distance(vector1,vector2):
	distance = 0
	for i in range(len(vector1)):
		distance += (vector2[i]-vector1[i])**2
	return math.sqrt(distance)
def cosine_similarity(vector1,vector2):
	vectorA = np.array(vector1)
	vectorB = np.array(vector2)
	cosine = (np.dot(vector1,vector2))/((math.sqrt(np.dot(vector1,vector1))) * np.sqrt((np.dot(vector2,vector2))))
	return cosine
"""