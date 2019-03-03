import numpy as np
import re
import math

#Funcion para separar las palabras sin signos de puntuacion
def extract_words(sentence):
    words = re.sub("[^\w]", " ",  sentence).split()
    words_cleaned = [w.lower() for w in words]
    return words_cleaned

def tokenize_sentences(sentences):
	words=[]
	for sentence in sentences:
		aux_words = extract_words(sentence)
		words.extend(aux_words)

	words=sorted(list(set(words)))
	return words
def evaluate_text(bag,text):
	bagofWords = []
	for b in bag:
		if b in text:
			bagofWords.append(1)
		else:
			bagofWords.append(0)
	return bagofWords

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

def main():
	#Abrimos el archivo uno
	text1=open("ejemplo.txt","r")
	sentences_text1 = text1.read().lower()
	#Abrimos el archivo dos
	text2=open("ejemplo1.txt","r")
	sentences_text2 = text2.read().lower()
	#Creamos la bolsa de palabras
	bag = tokenize_sentences([sentences_text1,sentences_text2])
	
	#Obtenemos las bolsas de palabras de cada texto
	bagofWords_text1 = evaluate_text(bag,sentences_text1)
	bagofWords_text2 = evaluate_text(bag,sentences_text2)
	print("--- Bolsa de palabras ---")
	print(bag)
	print("--- Bolsa texto uno ---")
	print(bagofWords_text1)
	print("--- Bolsa texto dos")
	print(bagofWords_text2)

	print("-----Similitud-----")
	#Calculamos la similitud euclidiana
	simEuclidean = euclidean_distance(bagofWords_text1,bagofWords_text2)
	print("Distancia euclidiana: " +str(simEuclidean))
	#Calculamos la similitud coseno
	simCos = cosine_similarity(bagofWords_text1,bagofWords_text2)
	print ("Similitud coseno: " + str(simCos))


main()

