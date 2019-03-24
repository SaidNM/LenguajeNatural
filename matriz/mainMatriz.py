import funciones as fnMatriz

def main():
	#Abrimos el archivo uno
	text1=open("ejemplo1.txt","r")
	sentences_text1 = text1.read().lower()
	sentences_text1 = fnMatriz.extract_words(sentences_text1)
	#Abrimos el archivo dos
	text2=open("ejemplo2.txt","r")
	sentences_text2 = text2.read().lower()
	sentences_text2 = fnMatriz.extract_words(sentences_text2)
	#Abrimos el archivo tres
	text3 = open("ejemplo.txt","r")
	sentences_text3 = text3.read().lower()
	sentences_text3 = fnMatriz.extract_words(sentences_text3)
	#Creamos nuestro vocabulario (Diccionario key = palabra : value= idf)
	vocabulary = fnMatriz.tokenize_sentences([sentences_text1,sentences_text2,sentences_text3])
	print("----- Vocabulario -----")
	print(vocabulary)

	#Obtenemos los diciconario de cada cada texto (Diccionario key = palabra : value = tf)
	matrix = fnMatriz.list_dictionary([sentences_text1,sentences_text2,sentences_text3])

	print("--- matriz TF ---")
	fnMatriz.showMatriz(vocabulary,matrix)
	
	print("-----Similitud-----")
	#Calculamos la similitud euclidiana
	#simEuclidean = euclidean_distance(bagofWords_text1,bagofWords_text2)
	#print("Distancia euclidiana: " +str(simEuclidean))
	
	#Calculamos la similitud coseno
	
	#Enlistamos los valores de los tres diccionarios
	list_text1 = fnMatriz.create_list(vocabulary,matrix[0])
	list_text2 = fnMatriz.create_list(vocabulary,matrix[1])
	list_text3 = fnMatriz.create_list(vocabulary,matrix[2])


	simCos1_2 = fnMatriz.cosine_similarity(list_text1,list_text2)
	simCos1_3 = fnMatriz.cosine_similarity(list_text1,list_text3)
	simCos2_3 = fnMatriz.cosine_similarity(list_text2,list_text3)
	print ("Similitud coseno texto1-texto2: " + str(simCos1_2))
	print ("Similitud coseno texto1-texto3: " + str(simCos1_3))
	print ("Similitud coseno texto2-texto3: " + str(simCos2_3))
	
	text1.close()
	text2.close()
	text3.close()

main()