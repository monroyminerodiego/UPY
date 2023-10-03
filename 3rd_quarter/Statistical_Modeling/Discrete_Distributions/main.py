if __name__ == "__main__":
    from discrete_distributions import DiscreteDistributions
    dist = DiscreteDistributions()
    again = True
    while again:
        print(f"""{'*'*15} Discrete Distribution Menu {'*'*15}
        1. Uniform Distribution
        2. Poisson Distribution
        3. Binomial Distribution
        4. Bernoulli Distribution
        5. Geometric Distribution
        """)
        selection = input("Enter an option (1-5): ")

        if selection == "1":
            dist.Uniformdist()
        elif selection == "2":
            dist.Poissondist()
        elif selection == "3":
            dist.Binomialdist()
        elif selection == "4":
            dist.Bernoullidist()
        elif selection == "5":
            dist.Geometricdist()

        again = input('\n\nDo you want to try again? (Y/N): ')
        if (again.lower() != 'y') or (again.lower() != 'ye') or (again.lower() != 'yes'):
            print("I'll take that as if you want to exit!")
