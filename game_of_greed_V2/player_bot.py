""""
Create a Game of Greed Player Bots
ONLY use public methods
- Game class constructor and play method
- DO NOT INJECT CUSTOM ROLL FUNCTION
- GameLogic, all methods available
"""
import builtins
import re

from game_of_greed_V2.game import Game
from game_of_greed_V2.game_logic import GameLogic

Venom_th_Risker_xI_scor = 0
Second_player_scor = 0

class BasePlayer:
    def __init__(self):
        self.old_print = print
        self.old_input = input
        builtins.print = self._mock_print
        builtins.input = self._mock_input
        self.total_score = 0
        self.keepers = 0
        self.rollNum = 0

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

        # print(
        #     f"{num_games} games (maybe) played with average score of {mega_total // num_games}"
        # )


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
            # self.old_print(prompt, 'y')
            return "y"
        elif prompt.startswith("Enter dice to keep (no spaces), or (q)uit:"):
            scorers = GameLogic.get_scorers(self.roll)
            self.keepers = "".join([str(ch) for ch in scorers])
            
            if self.roll.__len__() - self.keepers.__len__() == 0:
                if self.keepers.__len__() == 6:
                    
                    self.rollNum = 0
                else:
                    self.rollNum = 4
                return self.keepers
            elif self.roll.__len__() - self.keepers.__len__() <= 3 and self.roll.__len__() - self.keepers.__len__() > 0:
                self.rollNum = 4
                return self.keepers

            return self.keepers
        elif prompt.startswith("(r)oll again, (b)ank your points or (q)uit "):
            self.old_print(prompt)
            if self.rollNum < 3:
                if self.keepers.__len__() == 6:
                    return 'r'
                elif self.keepers.__len__() == 5 or self.keepers.__len__() == 4:
                    self.rollNum = 0
                    return 'b'
                elif self.keepers.__len__() < 4:
                    self.rollNum += 1
                    return 'r'
            else:
                self.rollNum = 0
                return "b"

            # self.old_print(self.keepers)
        else:
            raise ValueError(f"Unrecognized prompt {prompt}")



if __name__ == "__main__":
    # Venom_th_Risker_xI.play(10)

