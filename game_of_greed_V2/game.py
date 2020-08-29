import os
import sys

print(sys.path)

from game_of_greed_V2.game_logic import GameLogic , Banker



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

        print("Welcome to Game of Greed")

        prompt = "Wanna play?"

        self.choice(prompt.strip(), self.start_game, self.decline_game)

    def choice(self, prompt, accept, decline):

        response = input(prompt)

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

        self.quit_game()

    def quit_game(self):

        # print(f"Thanks for playing. You earned {self.banker.balance} points")

        sys.exit()

    def start_round(self, round, num_dice=6):

        print(f"Starting round {round}")

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
                self.quit_game()

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
            print("Cheater!!! Or possibly made a typo...")
            print(",".join([str(i) for i in roll]))
            keeper_string = input("Enter dice to keep (no spaces), or (q)uit: ")
            if keeper_string.startswith("q"):
                self.quit_game()

            keepers = [int(ch) for ch in keeper_string]

        return keepers


def clear():
    # stretch goal to allow user to clear terminal mid game

    # os.system("cls" if os.name == "nt" else "clear")
    pass


if __name__ == "__main__":
    game = Game()
    game.play()
