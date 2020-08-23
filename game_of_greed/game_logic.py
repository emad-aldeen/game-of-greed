from collections import Counter
import random

all_rules = {
    '(1, 1)': 100,
    '(1, 2)': 200,
    '(1, 3)': 1000,
    '(1, 4)': 2000,
    '(1, 5)': 3000,
    '(1, 6)': 4000,
    '(2, 3)': 200,
    '(2, 4)': 400,
    '(2, 5)': 600,
    '(2, 6)': 800,
    '(3, 3)': 300,
    '(3, 4)': 600,
    '(3, 5)': 900,
    '(3, 6)': 1200,
    '(4, 3)': 400,
    '(4, 4)': 800,
    '(4, 5)': 1200,
    '(4, 6)': 1600,
    '(5, 1)': 50,
    '(5, 2)': 100,
    '(5, 3)': 500,
    '(5, 4)': 1000,
    '(5, 5)': 1500,
    '(5, 6)': 2000,
    '(6, 3)': 600,
    '(6, 4)': 1200,
    '(6, 5)': 1800,
    '(6, 6)': 2400,
}

class GameLogic():
    
    @staticmethod
    def calculate_score(tuble): 
        '''
        function to calculate the score of the 'dic roll':
            input ---> tuble containing dic roll numbers
            output >> integer equal the dic roll numbers based by the rules of the game
        '''
        result = 0
        tu_length = len(Counter(tuble).most_common())
        if tu_length == 6 or (tu_length == 3 and Counter(tuble).most_common()[0][1] == 2 and Counter(tuble).most_common()[1][1] == 2 and Counter(tuble).most_common()[2][1] == 2):
            return 1500 
        else:
            for i in range(len(Counter(tuble).most_common())):
                result += GameLogic.search(str(Counter(tuble).most_common()[i]))
        return result
    
    @staticmethod
    def search(value):
        '''
        function designed only for search inside teh rulls dectionary:
            input ---> key to search for it in dictionary and it must be in tuble format
            output >> value of the inputed key..
        '''
        try:
            all_rules[value]
        except:
            return 0
        else:
            return all_rules[value]
    
    @staticmethod
    def roll_dice(n):
        '''
        function used for create random integer(1,6) number based on argument:
            input -->int number(4)
            output-->tuple contain random number example= (2,4,5,1)
        '''
        tup=[]
        for i in range(n): 
            tup.append(random.randint(1,6))
        return(tuple(tup))




class Banker(): 
    
    def __init__(self) : 
        self.shelved = 0 
        self.balance = 0



    
    def shelf (self,points) :
        self.shelved += points 
    

    def bank (self) :

        self.balance += self.shelved 
        self.shelved = 0

        return self.balance



    def clear_shelf(self) :

        self.shelved = 0



if __name__ == "__main__":
    # print(GameLogic.calculate_score((5, 5)))
    # print()
    new_bank = Banker()
    # print(new_bank.shelf(5))
    new_bank.shelf(100)
    new_bank.shelf(50)
    print(new_bank.shelved)


