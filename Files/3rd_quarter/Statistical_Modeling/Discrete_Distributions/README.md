# Discrete Distributions

## Instructions given by teacher 
Create a .py class in python called DiscreteDistributions With all distributions as a method.

## Explanation of files
### - discrete_distributions.py  
File where we created our class with 5 diferent methods:
<table style="text-align:center;">
    <tr>
        <th>Method Name</th>
        <th>Inputs</th>
        <th>Output</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>
            Uniformdist()
        </td>
        <td>
            - n [int]: Number of trials<br>
            - x [float]: Number of successes
        </td>
        <td>
            - result [float]: The result of the Uniform distribution calculus
        </td>
        <td>
            Function to calculate the Uniform Distribution
        </td>
    </tr>
    <tr>
        <td>
            Poissondist()
        </td>
        <td>
            - x [float]: Probability of x. <br>
            - miu [float]: The expected value of x. 
        </td>
        <td>
            - result [float]: The result of the Poisson distribution calculus
        </td>
        <td>
            Function to calculate the Poisson Distribution
        </td>
    </tr>
    <tr>
        <td>
            Binomialdist()
        </td>
        <td>
            - n [int]: Number of trials <br>
            - x [float]: Number of successes <br>
            - p [float]: Probability of success <br>
            - q [float]: Probability of failure
        </td>
        <td>
            - result [float]: The result of the Binomial distribution calculus
        </td>
        <td>
            Function to calculate the Binomial Distribution
        </td>
    </tr>
    <tr>
        <td>
            Bernoullidist()
        </td>
        <td>
            - x [float]: Number of successes <br>
            - p [float]: Probability of success
        </td>
        <td>
            - result [float]: The result of the Bernoulli distribution calculus
        </td>
        <td>
            Function to calculate the Bernoulli Distribution
        </td>
    </tr>
    <tr>
        <td>
            Geometricdist()
        </td>
        <td>
            - x [float]: Number of successes <br>
            - p [float]: Probability of success
        </td>
        <td>
            - result [float]: The result of the Geometric distribution calculus
        </td>
        <td>
            Function to calculate the Geometric Distribution
        </td>
    </tr>
</table>

### - main.py
File in which we test the class methods from 'discrete_distributions.py' file. It also prints the menu and validates if user wants to try again the script.


## Made By
- Juan Antonio Cel Vazquez
- Sergio Johanan Barrera Chan
- Ariel Joel Buenfil Góngora
- Diego Monroy Minero