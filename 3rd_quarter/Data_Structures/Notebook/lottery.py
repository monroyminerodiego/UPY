'''
Generate 40 lottery cards with 16 different images, selecting them from the 54 available cards
'''
class Lottery:
    def __init__(self,num_layers:int,images_per_layer:int):
        '''
        
        '''
        self.num_layers = num_layers
        self.images_per_layer = images_per_layer
        self.combinations = self.__generate_combinations()
        

    def __generate_combinations(self):
        '''
        
        '''
        unsorted_final_combinations, sorted_final_combinations = [], []
        while len(unsorted_final_combinations) < self.num_layers:
            unsorted_combination = []
            while len(unsorted_combination) < self.images_per_layer:
                number = random.randint(1,54)
                if not(number in unsorted_combination):
                    unsorted_combination.append(number)
            
            sorted_combination = '-'.join([str(x) for x in sorted(unsorted_combination)])
            if not(sorted_combination in sorted_final_combinations):
                unsorted_final_combinations.append(unsorted_combination)
                sorted_final_combinations.append(sorted_combination)
        return unsorted_final_combinations, sorted_final_combinations
            
    def __str__(self):
        string = f'{"*"*15} Lottery {"*"*15}\nCards:\n'
        i = 1
        for _ in sorted(self.combinations[1], key=lambda tuple: tuple[0]):
            string += f'{i}.- {_}\n'
            i += 1
        return string

if __name__ == '__main__':
    import os; os.system('cls')
    import random
    lottery = Lottery(40,16)
    print(lottery)
    