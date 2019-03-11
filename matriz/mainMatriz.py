import funciones as fnMatriz

def main():
	#Abrimos el archivo uno
	text1=open("ejemplo1.txt","r")
	sentences_text1 = text1.read().lower()
	#Abrimos el archivo dos
	text2=open("ejemplo2.txt","r")
	sentences_text2 = text2.read().lower()
	#Abrimos el archivo tres
	text3 = open("ejemplo.txt","r")
	sentences_text3 = text3.read().lower()
	#Creamos la bolsa de palabras
	bag = fnMatriz.tokenize_sentences([sentences_text1,sentences_text2])
	print("----- palabras -----")
	print(bag)
	#Obtenemos los vectores TF de cada texto
	matriz = fnMatriz.matrizTF(bag,[sentences_text1,sentences_text2])

	print("--- matriz TF ---")
	fnMatriz.showMatriz(bag,matriz)
	print("-----Similitud-----")
	#Calculamos la similitud euclidiana
	#simEuclidean = euclidean_distance(bagofWords_text1,bagofWords_text2)
	#print("Distancia euclidiana: " +str(simEuclidean))
	#Calculamos la similitud coseno
	#simCos = cosine_similarity(bagofWords_text1,bagofWords_text2)
	#print ("Similitud coseno: " + str(simCos))

main()