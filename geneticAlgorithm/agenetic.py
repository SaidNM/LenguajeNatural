
import random as rnd
import time as tm


class Cromosoma:
    def __init__(self, genes, fitness):
        self.genes=genes
        self.fitness=fitness

    def len(self):
        return len(self.genes)

    def __str__(self):
        s="%s %d" % (" ".join(map(str, self.genes)), self.fitness)
        s2=[]
        n=len(self.genes)
        for i in range(n):
            s2.append(list("-"*n))
            for k in range(n):
                if self.genes[k]==i:  ## el numero de casilla en el cual se encuentra la R
                    s2[i][k]="R"
            s2[i]=" ".join(s2[i])
        print(s2)
        print("\n")
        return "\n".join(s2)+"\nfitness: " + str(self.fitness)

class AGenetico:

    def __init__(self, casillas):
        self.casillas=casillas
        self.genes=range(casillas)

    def fidoneidad(self, genes):
        fitness=0
        i=0
        for k in range(len(genes)):
            for i in range(len(genes)):
                if genes[k]==genes[i]:   # reina en horizontal
                    continue
                elif((k-genes[k])==(i-genes[i])):
                	continue
                elif((k+genes[k])==(i+genes[i])):
                    continue
                else:
                    fitness+=1
        return fitness

    def newParent(self):
        genes=rnd.sample(self.genes, self.casillas)
        fitness=self.fidoneidad(genes)
        return Cromosoma(genes, fitness)

    def reproducir(self, x, y):
        c=rnd.randint(0, x.len())
        genes=x.genes[:c]+y.genes[c:]
        fitness=self.fidoneidad(genes)
        return Cromosoma(genes, fitness)

    def mutar(self, hijo):
        n=rnd.randint(0, hijo.len()-1)
        genes=hijo.genes
        genes[n]=-1
        genX=genY=max(genes)
        while genX in genes and genY in genes:
            genX, genY = rnd.sample(self.genes, 2)
        genes[n]= genX if genX in genes else genY
        hijo.fitness=self.fidoneidad(genes)
        hijo.genes=genes
        return hijo

    def seleccion(self, poblacion):
        if len(poblacion)>0:
            return rnd.choice(poblacion)
        else:
            return self.newParent()


    def algoritmo(self, poblacion):

        while True:
            npobla=[]
            for i in range(len(poblacion)):
                x=self.seleccion(poblacion)
                y=self.seleccion(poblacion)
                hijo=self.reproducir(x, y)
                if rnd.randint(1, 20)<3:
                    hijo=self.mutar(hijo)
                npobla.append(hijo)
                if npobla[i].fitness>=(self.casillas*self.casillas-self.casillas):
                    return npobla[i]
            poblacion=npobla


    def run(self):
        poblacion=[]
        for i in range(350):
            poblacion.append(self.newParent())
        print (self.algoritmo(poblacion))

    def tablaMejores():
    	


if __name__=="__main__":
    for n in [8]:
        alg=AGenetico(n)
        alg.run()
