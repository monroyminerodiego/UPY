import os
if __name__ == "__main__":
    from discrete_distributions import DiscreteDistributions
    dist = DiscreteDistributions()
    again = True
    while again:
        os.system('cls')
        menu = {"1":"Uniform","2":"Poisson","3":"Binomial","4":"Bernoulli","5":"Geometric",}
        print(f"""{'*'*15} Discrete Distribution Menu {'*'*15}
    1. Uniform Distribution
    2. Poisson Distribution
    3. Binomial Distribution
    4. Bernoulli Distribution
    5. Geometric Distribution
        """)
        selection = input("Enter an option (1-5): ")

        if selection == "1":
            result = dist.Uniformdist(
                n = int(input("\nEnter the number of trials: ")),
                x = float(input("Enter the number of successes: "))
            )
        elif selection == "2":
            result = dist.Poissondist(
                x = float(input("\nEnter the number of successes: ")),
                miu = float(input("Enter the expected value of x: "))
            )
        elif selection == "3":
            result = dist.Binomialdist(
                n = int(input("\nEnter the number of trials: ")),
                x = float(input("Enter the number of successes: ")),
                p = float(input("Enter the probability of success: ")),
                q = float(input("Enter the probability of failure: "))
            )
        elif selection == "4":
            result = dist.Bernoullidist(
                x = float(input("\nEnter the number of successes: ")),
                p = float(input("Enter the probability of success: "))
            )
        elif selection == "5":
            result = dist.Geometricdist(
                x = float(input("\nEnter the number of successes: ")),
                p = float(input("Enter the probability of success: "))
            )

        print(f'\nThe result of the {menu[selection]} Distribution, according to the parameters, is: {result:.04f}')

        again = input('\n\nDo you want to try again? (Y/N): ')
        if not((again.lower() == 'y') or (again.lower() == 'ye') or (again.lower() == 'yes')):
            print("I'll take that as if you want to exit!\n\nGoodbye...! :D")
            break
