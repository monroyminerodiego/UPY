import math

class DiscreteDistributions:
    
    def __init__(self):
        self.n = float      #Number of trials
        self.x = float      #Number of successes / probability of x
        self.p = float      #Probability of success
        self.q = float      #Probability of failure
        self.miu = float

    def Uniformdist(self):
        """
        Function to calculate the Uniform Distribution

        Inputs
        - n <class 'int'>: Number of trials
        - x <class 'float'>: Number of successes

        Output
        - result <class 'float'>: The result of the uniform distribution calculus
        """
        self.n = float(input("Introduzca el número de intentos: "))
        self.x = float(input("Introduzca el número de éxitos: "))
        self.fdex = (1) / (self.n)
        self.result = self.fdex * self.x
        return self.result
        def mean(self):
            self.uniform_mean = (self.n + 1) / 2
    
        
    
    def Poissondist(self):
        """
        Function to calculate the Poisson Distribution

        Inputs
        - x <class 'float'>: Probability of x.
        - miu <class 'float'>: The expected value of x. 

        Output
        - result <class 'float'>: The result of the Poisson distribution calculus
        """
        self.x = int(input("Introduzca la probabilidad de x: "))
        self.miu = float(input("Introduzca el valor esperado de x: "))
        self.result = ((math.e**-self.miu) * (self.miu**self.x)) / (math.factorial(self.x))
        return self.result
        
    
    def Binomialdist(self):
        """
        Function to calculate the Binomial Distribution

        Inputs
        - n <class 'int'>: Number of trials
        - x <class 'float'>: Number of successes
        - p <class 'float'>: Probability of success
        - q <class 'float'>: Probability of failure 

        Output
        - result <class 'float'>: The result of the Binomial distribution calculus
        """
        self.n = int(input("Introduzca el número de intentos: "))
        self.x = int(input("Introduzca el número de éxitos: "))
        self.p = float(input("Introduzca la probabilidad de éxito: "))
        self.q = float(input("Introduzca la probabilidad de fallo: "))
        self.combination_nx = (math.factorial(self.n)) / (math.factorial(self.x)) * (math.factorial(self.n - self.x))
        self.result = float((self.combination_nx) * ((self.p**(self.x) * (self.q**(self.n - self.x)))))
        return self.result

    def Bernoullidist(self):
        """
        Function to calculate the Bernoulli Distribution

        Inputs
        - x <class 'float'>: Number of successes
        - p <class 'float'>: Probability of success

        Output
        - result <class 'float'>: The result of Bernoulli distribution calculus
        """
        self.x = float(input("Introduzca 1 si hubo éxito, introduzca 0 si hubo fracaso: "))
        self.p = float(input("Introduzca la probabilidad de éxito: "))
        if self.x == True:
            self.result = self.p**1 * ((1 - self.p)**(1-1))
        else :
            self.result = self.p**0 * ((1 - self.p)**(1-0))

        return self.result

    
    def Geometricdist (self):
        """
        Function to calculate the Geometric Distribution

        Inputs
        - x <class 'float'>: Number of successes
        - p <class 'float'>: Probability of success

        Output
        - result <class 'float'>: The result of the Geometric distribution calculus
        """
        self.x = float(input("Introduzca el número de intentos en el cual se quiere averiguar el experimento: "))
        self.p = float(input("Introduzca la probabilidad de éxito: "))
        self.result = self.p * (1 - self.p)**(self.x - 1)
        return self.result
