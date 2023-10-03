import math

class DiscreteDistributions:
    def Uniformdist(self,n=int,x=float):
        """
        Function to calculate the Uniform Distribution

        Inputs
        - n <class 'int'>: Number of trials
        - x <class 'float'>: Number of successes

        Output
        - result <class 'float'>: The result of the uniform distribution calculus
        """
        self.fdex = (1) / (n)
        self.result = self.fdex * x
        return self.result
    
        
    
    def Poissondist(self,x=float,miu=float):
        """
        Function to calculate the Poisson Distribution

        Inputs
        - x <class 'float'>: Probability of x.
        - miu <class 'float'>: The expected value of x. 

        Output
        - result <class 'float'>: The result of the Poisson distribution calculus
        """
        self.result = ((math.e**-miu) * (miu**x)) / (math.factorial(int(x)))
        return self.result
        
    
    def Binomialdist(self,n=int,x=float,p=float,q=float):
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
        self.combination_nx = (math.factorial(int(n))) / (math.factorial(int(x))) * (math.factorial(abs(int(n) - int(x))))
        self.result = float((self.combination_nx) * ((p**(x) * (q**(n - x)))))
        return self.result

    def Bernoullidist(self,x=float,p=float):
        """
        Function to calculate the Bernoulli Distribution

        Inputs
        - x <class 'float'>: Number of successes
        - p <class 'float'>: Probability of success

        Output
        - result <class 'float'>: The result of Bernoulli distribution calculus
        """
        if x == True:
            self.result = p**1 * ((1 - p)**(1-1))
        else :
            self.result = p**0 * ((1 - p)**(1-0))

        return self.result

    
    def Geometricdist (self,x=float,p=float):
        """
        Function to calculate the Geometric Distribution

        Inputs
        - x <class 'float'>: Number of successes
        - p <class 'float'>: Probability of success

        Output
        - result <class 'float'>: The result of the Geometric distribution calculus
        """
        self.result = p * (1 - p)**(x - 1)
        return self.result
