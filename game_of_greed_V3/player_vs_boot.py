"""
Create a Game of Greed Player Bots
ONLY use public methods
- Game class constructor and play method
- DO NOT INJECT CUSTOM ROLL FUNCTION
- GameLogic, all methods available
"""
import builtins
import re
import os
import sys

from game_of_greed_V3.game_logic import GameLogic , Banker

venomThRiskerXI_score = 0
second_plyer_score = 0
msg = 'Unfortuntly the Bot Wins!!'

class Game:
    """Class for Game of Greed application
    """

    def __init__(self, roller=None, num_rounds=1):

        self._roller = roller or GameLogic.roll_dice
        self.banker = Banker()
        self.num_rounds = num_rounds
        self.round_num = 0

    def play(self):
        """
        Entry point for playing (or/not) a game
        """

        # print("Welcome to Game of Greed")

        # prompt = "Wanna play?"

        self.choice(self.start_game, self.decline_game)

    def choice(self, accept, decline):

        response = 'y'

        if response == "y" or response == "yes":

            accept()

        else:

            decline()

    def decline_game(self):
        print("OK. Maybe another time")

    def start_game(self):

        self.round_num = 1

        while self.round_num <= self.num_rounds:

            self.start_round(self.round_num)

            self.round_num += 1

            print(f"Total score is {self.banker.balance} points")
            global second_plyer_score
            second_plyer_score += self.banker.balance

        self.quit_game()

    def quit_game(self):
        return 

    def start_round(self, round, num_dice=6):

        # print(f"Starting round {round}")

        round_score = 0

        while True:

            roll = self.roll_dice(num_dice)

            if self.got_zilch(roll):
                break

            keepers = self.handle_keepers(roll)

            roll_again_response = input("(r)oll again, (b)ank your points or (q)uit ")

            if roll_again_response == "q":

                self.quit_game()

                return

            elif roll_again_response == "b":

                round_score = self.banker.bank()

                break

            else:

                num_dice -= len(keepers)

                if num_dice == 0:

                    num_dice = 6

        print(f"You banked {str(round_score)} points in round {round}")

    def handle_keepers(self, roll):

        while True:
            keeper_string = input("Enter dice to keep (no spaces), or (q)uit: ")

            if keeper_string.startswith("q"):
                sys.exit()

            keepers = self.gather_keepers(roll, keeper_string)

            roll_score = self.calculate_score(keepers)

            if roll_score == 0:
                print("Must keep at least one scoring dice")
            else:
                break

        self.banker.shelf(roll_score)

        print(
            f"You have {self.banker.shelved} unbanked points and {len(roll) - len(keepers)} dice remaining"
        )

        return keepers

    def roll_dice(self, num):

        print(f"Rolling {num} dice...")

        roll = self._roller(num)

        print(",".join([str(i) for i in roll]))

        return roll

    def got_zilch(self, roll):

        initial_score = self.calculate_score(roll)

        if initial_score == 0:

            print("Zilch!!! Round over")

            self.banker.clear_shelf()

            return True

        return False

    def calculate_score(self, roll):
        return GameLogic.calculate_score(roll)

    def keep_scorers(self, roll):
        return GameLogic.get_scorers(roll)

    def gather_keepers(self, roll, keeper_string):

        keepers = [int(ch) for ch in keeper_string]

        while not GameLogic.validate_keepers(roll, keepers):
            print("Cheater!!!")
            global venomThRiskerXI_score, msg, second_plyer_score
            venomThRiskerXI_score += 100000
            second_plyer_score = -1000000000000
            msg = "you little cheater!! \n\n you lost and the bot wins.. \n \n dont cheat again loser :/"
            print(",".join([str(i) for i in roll]))
            keeper_string = input("Enter dice to keep (no spaces), or (q)uit: ")
            if keeper_string.startswith("q"):
                sys.exit()

            keepers = [int(ch) for ch in keeper_string]

        return keepers


class BasePlayer:
    def __init__(self):
        self.old_print = print
        self.old_input = input
        builtins.print = self._mock_print
        builtins.input = self._mock_input
        self.total_score = 0
        self.keepers = 0
        self.rollNum = 0
        self.ven_score = 0

    def reset(self):
        builtins.print = self.old_print
        builtins.input = self.old_input

    # The default behaviour
    def _mock_print(self, *args, **kwargs):
        self.old_print(*args, **kwargs)

    def _mock_input(self, *args, **kwargs):
        return self.old_input(*args, **kwargs)

    @classmethod
    def play(cls, num_games=1):

        mega_total = 0

        for i in range(num_games):
            player = cls()
            game = Game() # doesn't pass a mock roller
            try:
                game.play()
            except SystemExit:
                # in game system exit is fine
                # because that's how they quit.
                pass

            mega_total += player.total_score
            player.reset()


class Venom_th_Risker_xI(BasePlayer):
    def __init__(self):
        super().__init__()
        self.roll = None

    

    def _mock_print(self, *args, **kwargs):
        first_arg = args[0]
        first_char = first_arg[0]
        if first_char.isdigit():
            self.roll = tuple(int(char) for char in first_arg.split(","))
        elif first_arg.startswith("Thanks for playing."):
            self.total_score = int(re.findall(r"\d+", first_arg)[0])
        self.old_print(first_arg)

    def _mock_input(self, *args, **kwargs):
        prompt = args[0]
        if prompt.startswith("Wanna play?"):
            return "y"
        elif prompt.startswith("Enter dice to keep (no spaces), or (q)uit:"):
            scorers = GameLogic.get_scorers(self.roll)
            self.keepers = "".join([str(ch) for ch in scorers])
            
            if self.roll.__len__() - self.keepers.__len__() == 0:
                if self.keepers.__len__() == 6:
                    self.rollNum = 0
                else:
                    self.rollNum = 4
                self.ven_score += GameLogic.calculate_score(scorers)
                return self.keepers
            elif self.roll.__len__() - self.keepers.__len__() <= 3 and self.roll.__len__() - self.keepers.__len__() > 0:
                self.rollNum = 4
                self.ven_score += GameLogic.calculate_score(scorers)
                return self.keepers

            self.ven_score += GameLogic.calculate_score(scorers)
            return self.keepers
        elif prompt.startswith("(r)oll again, (b)ank your points or (q)uit "):
            self.old_print(prompt)
            if self.rollNum < 3:
                if self.keepers.__len__() == 6:
                    return 'r'
                elif self.keepers.__len__() == 5 or self.keepers.__len__() == 4:
                    self.rollNum = 0
                    global venomThRiskerXI_score
                    venomThRiskerXI_score += self.ven_score
                    return 'b'
                elif self.keepers.__len__() < 4:
                    self.rollNum += 1
                    return 'r'
            else:
                self.rollNum = 0
                venomThRiskerXI_score += self.ven_score
                return "b"
        else:
            raise ValueError(f"Unrecognized prompt {prompt}")


if __name__ == "__main__":
    venomThRiskerXI_score = 0
    second_plyer_score = 0
    new_game = Game()
    gg_round = 0


    print("\n******************************** Welcome to game of greed ********************************\n\nRules:\n- you will play aginst our Bot (Venom th Risker 8|)\n- every round you will get 6 dice and you will choice witch is high poenty for you..\n- first who reach 1200 point will win the game\n- Don't..Don't..Don't try to cheat :|")

    response = input("\n\n want to play?  \n>")
    if response == 'yes' or response == 'y':
        while True:
            if second_plyer_score >= 1200:
                print('\n\n/////////////////////////////////// We have Winer.. /////////////////////////////////////////')
                print('\n\nCongrats You Win!!\n\n')
                print(f'Bot score is {venomThRiskerXI_score} and your score is {second_plyer_score}')
                break
            elif venomThRiskerXI_score >= 1200:
                print('\n\n/////////////////////////////////// We have Winer.. /////////////////////////////////////////')
                print(f'\n\n{msg}\n\n')
                print(f'Bot score is {venomThRiskerXI_score} and your score is {second_plyer_score}')
                break
            else:
                gg_round += 1
                print(f'\n*********************************** Round {gg_round} **********************************')
                print('\n/////////////////////////////////// Your Turn /////////////////////////////////////////')
                new_game.play()
                print('\n/////////////////////////////////// Bot Turn /////////////////////////////////////////')
                Venom_th_Risker_xI.play(1)
    else:
        print('thank you for visiting us.. :)')
