import math

class DiscreteDistributions:
    
    def __init__(self):
        self.n = float      #Number of trials
        self.x = float      #Number of successes / probability of x
        self.p = float      #Probability of success
        self.q = float      #Probability of failure
        self.miu = float

    def Uniformdist(self):
        self.n = float(input("Introduzca el número de intentos: "))
        self.x = float(input("Introduzca el número de éxitos: "))
        self.fdex = (1) / (self.n)
        self.uniformdist_result = self.fdex * self.x
        print("La distribución uniforme discreta es: ", self.uniformdist_result)
        def mean(self):
            self.uniform_mean = (self.n + 1) / 2
    
        
    
    def Poissondist(self):
        self.x = int(input("Introduzca la probabilidad de x: "))
        self.miu = float(input("Introduzca el valor esperado de x: "))
        self.poissondist_result = ((math.e**-self.miu) * (self.miu**self.x)) / (math.factorial(self.x))
        print("La distribución de Poisson es: ", self.poissondist_result)
        
    
    def Binomialdist(self):
        self.n = int(input("Introduzca el número de intentos: "))
        self.x = int(input("Introduzca el número de éxitos: "))
        self.p = float(input("Introduzca la probabilidad de éxito: "))
        self.q = float(input("Introduzca la probabilidad de fallo: "))
        self.combination_nx = (math.factorial(self.n)) / (math.factorial(self.x)) * (math.factorial(self.n - self.x))
        self.binomialdist_result = float((self.combination_nx) * ((self.p**(self.x) * (self.q**(self.n - self.x)))))
        print("La distribución binomial es: ", self.binomialdist_result)

    def Bernoullidist(self):
        self.x = float(input("Introduzca 1 si hubo éxito, introduzca 0 si hubo fracaso: "))
        self.p = float(input("Introduzca la probabilidad de éxito: "))
        if self.x == True:
            self.bernoullidist_success = self.p**1 * ((1 - self.p)**(1-1))
            print("La distribución de Bernoulli es: ", self.bernoullidist_success)
        else :
            self.bernoullidist_failure = self.p**0 * ((1 - self.p)**(1-0))
            print("La distribución de Bernoulli es: ", self.bernoullidist_failure)

    
    def Geometricdist (self):
        self.x = float(input("Introduzca el número de intentos en el cual se quiere averiguar el experimento: "))
        self.p = float(input("Introduzca la probabilidad de éxito: "))
        self.geometricdist_result = self.p * (1 - self.p)**(self.x - 1)
        print("La distribución geométrica es: ", self.geometricdist_result)
