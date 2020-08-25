from collections import Counter
from game_of_greed.game_logic import *
import sys

class Game:

    def __init__(self, roller = GameLogic.roll_dice):
        self.roller= roller

    @staticmethod
    def print_roll(roll):
        '''
        it only print the roll in formated way:
            input ---> tuple of roll numbers
            output >> printing the rool in formated way
        '''
        roll_as_string = [str(i) for i in roll]
        to_be_printed = ','.join(roll_as_string)
        print(to_be_printed)
    
    printing_total = True

    @staticmethod
    def check_pair__inpValuble(inputs):            
        '''
        it cheaks the user input if it is pairs or in order "1 - 6" then every input has value on the "game_logic.all_rules"..
            input ---> list of user inputs
            output >> 0 for False - 1 for True
        '''

        inputs_most_common = Counter(inputs).most_common()
        tuple_of_inputs = Counter(tuple(inputs)).most_common()

        if len(inputs) == 6:
        # chek if input in order 1 - 6 ..
            for i in range(6):
                if inputs_most_common[i][1] != 1:
                    break
                return 1

        # lets cheak if input is pairs..
            for i in range(len(inputs_most_common)):
                if inputs_most_common[i][1] != 2:
                    break
                return 1
                                    
    # cheak if all inputs return values..
        for i in tuple_of_inputs:
            res = []

            for j in inputs:
                if j == i[0]:
                    res.append(j)

            if GameLogic.calculate_score(tuple(res)) == 0:
                Game.printing_total = False
                return 0
        return 1


    @staticmethod
    def check_if_input_notExist(inputs, roll):
        '''
        it cheaks the user input if every number is really exist in the roll..
            input ---> list of user inputs
            output >> 0 for False - 1 for True
        '''
        res = 0
        roll_most_common = Counter(roll).most_common()
        inputs_most_common = Counter(inputs).most_common()

        
        for i in range(len(inputs_most_common)):
            
            if inputs_most_common[i][1] > 1:

                for j in range(len(roll_most_common)):

                    if roll_most_common[j][0] == inputs_most_common[i][0]:

                        if roll_most_common[j][1] < inputs_most_common[i][1]:
                            Game.printing_total = False
                            return 0
                                            
            else:

                for i in range(len(inputs)):

                    if inputs[i] not in roll:
                        Game.printing_total = False
                        res = 0
                    else:
                        res = 1
                        
                return res

    @staticmethod
    def check_zilch(roll):
        '''
        lets cheak if your roll equal nothing!! & thats called "Zilch":
            input ---> list of user inputs
            output >> 0 for False - 1 for True
        '''
        if GameLogic.calculate_score(roll) == 0:
            return 0
        return 1
    
    @staticmethod
    def quiting_game(score):
        '''
        i dont know what do you think?
        '''
        if Game.printing_total:
            print(f"Total score is {score} points")

        print(f"Thanks for playing. You earned {score} points")




    def play(self):
        round = 1
        score = 0
        print("Welcome to Game of Greed")
        response = input("Wanna play?")
        
        if response == 'n':
            print("OK. Maybe another time")
        elif response == 'y':
            
            while True:
                num_dice = 6 
                print(f"Starting round {round}")
                print(f"Rolling {num_dice} dice...")
                roll = self.roller(num_dice) # get new roll
                # roll = [1,2,3,4,5,6]
                dice_score = 0 
                while True:
                    self.print_roll(roll)

                    test_zilch = Game.check_zilch(roll)

                    if test_zilch == 0:
                        print(f'Zilch!!! Round over\nYou banked 0 points in round {round}\nTotal score is {score} points')
                        round += 1
                        break # start new round
                    
                    what_next = input("Enter dice to keep (no spaces), or (q)uit: ")

                    if what_next == 'q' or what_next == 'quit':

                        Game.quiting_game(score)

                        sys.exit() # it quiting the whole game and stop the script
                    else:
 
                        inputs = [int(i) for i in what_next] # convert input to intger list

                        test_1 = Game.check_if_input_notExist(inputs, roll)
                        test_2 = Game.check_pair__inpValuble(inputs)

                        if test_1 == 0:
                            print('Cheater!!! Or possibly made a typo...')
                            continue

                        else:
                            if test_2 == 0:
                                print ('Cheater!!! Or possibly made a typo...')
                                continue

                            else:    
                                num_dice -= len(inputs) 
                                tupleing_inputs = tuple(inputs)
                                dice_score += GameLogic.calculate_score(tupleing_inputs)
                                bank_round = Banker()
                                bank_round.shelf(dice_score)
                                print(f'You have {bank_round.shelved} unbanked points and {num_dice} dice remaining')
                                
                                # roll = self.roller(num_dice) # why homie!!? :|

                                after_round = input("(r)oll again, (b)ank your points or (q)uit ")

                                if after_round == 'r' or after_round == 'roll':

                                    if len(inputs) == 6:
                                        num_dice = 6 # to get free roll if inputs was all valuble..

                                    roll = self.roller(num_dice) # get new roll
                                    print(f"Rolling {num_dice} dice...")
                                    continue

                                elif after_round == 'b' or after_round == 'bank':
                                    bank_round.bank()
                                    print(f'You banked {bank_round.balance} points in round {round}')
                                    score += bank_round.balance
                                    print(f'Total score is {score} points')
                                    round += 1
                                    break

                                elif after_round == 'q' or after_round == 'quit':
                                    
                                    Game.quiting_game(score)
                                    
                                    sys.exit()
 

if __name__=='__main__':
    game = Game()
    game.play()