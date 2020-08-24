from collections import Counter
from game_of_greed.game_logic import *

class Game:

    def __init__(self, roller=GameLogic.roll_dice):
        self.roller= roller

    @staticmethod
    def print_roll(roll):
        roll_as_string = [str(i) for i in roll]
        to_be_printed = ','.join(roll_as_string)
        print(to_be_printed)
    
    def play(self):
        round = 1
        score = 0
        print("Welcome to Game of Greed")
        response = input("Wanna play?")
        if response == 'n':
            print("OK. Maybe another time")
        elif response == 'y':
            c = True
            while c:
                num_dice = 6
                print(f"Starting round {round}")
                print(f"Rolling {num_dice} dice...")
                roll = self.roller(num_dice)
                x = True
                dice_score = 0 
                while x:
                    self.print_roll(roll)
                    what_next = input("Enter dice to keep (no spaces), or (q)uit: ")
                    if what_next == 'q' or what_next == 'quit':
                        print(f"Total score is {score} points")
                        print(f"Thanks for playing. You earned {score} points")
                        x = False
                        c = False
                        break
                    else:
                        inputs = [int(i) for i in what_next]

                        def check():
                            res = 0
                            m_C = Counter(roll).most_common()
                            r_C = Counter(inputs).most_common()
                            for i in range(len(r_C)):
                                if r_C[i][1] > 1:
                                    for j in range(len(m_C)):
                                        if m_C[j][0] == r_C[i][0]:
                                            if m_C[j][1] < r_C[i][1]:
                                                return 0                   
                                else:
                                    for i in range(len(inputs)):
                                        if inputs[i] not in roll:
                                            res = 0
                                        else:
                                            res = 1
                                    return res

                        def check2():

                            r = Counter(tuple(inputs)).most_common()
                            
                            for i in r:
                                res = []
                                for j in inputs:
                                    if j == i[0]:
                                        res.append(j)
                                if GameLogic.calculate_score(tuple(res)) == 0:
                                    return 0
                            return 1

                        m = check()
                        n = check2()
                        if m == 0:
                            print('False')
                            continue
                        else:
                            if n == 0:
                                print ('Cheater')
                                continue
                            else:
                                num_dice -= len(inputs)
                                tup_inputs = tuple(inputs)
                                dice_score += GameLogic.calculate_score(tup_inputs)
                                rounds = Banker()
                                rounds.shelf(dice_score)
                                print(f'You have {rounds.shelved} unbanked points and {num_dice} dice remaining')
                                roll = self.roller(num_dice)
                                after_round = input("(r)oll again, (b)ank your points or (q)uit ")
                                if after_round == 'r':
                                    print(f"Rolling {num_dice} dice...")
                                    continue
                                elif after_round == 'b':
                                    rounds.bank()
                                    print(f'You banked {rounds.balance} points in round {round}')
                                    score += rounds.balance
                                    print(f'Total score is {score} points')
                                    round += 1
                                    x = False

                                elif after_round == 'q':
                                    print(f"Total score is {score} points")
                                    print(f"Thanks for playing. You earned  {score} points")
                                    x = False
                                    c = False
                                    break
                

                # print()
    


if __name__=='__main__':
    # game = Game(GameLogic.roll_dice)
    game = Game()
    game.play()