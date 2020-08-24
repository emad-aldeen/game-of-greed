import builtins
from game_of_greed.game import *


class Flo:

    PROMPTS = (
        "Wanna play?",
        "(r)oll again, (b)ank your points or (q)uit ",
        "Enter dice to keep (no spaces), or (q)uit: ",
    )

    def __init__(self, path):
        self.path = path

        self.old_print = print
        self.old_input = input
        builtins.print = self._mock_print
        builtins.input = self._mock_input
        self.prints = ""

        self.responses = []
        self.rolls = []

        with open(self.path) as file:
            for line in file.readlines():

                # gather prompt responses
                for prompt in self.PROMPTS:
                    if line.startswith(prompt):
                        response = line.split(prompt)[1].strip()
                        self.responses.append(response)

                # gather rolls
                if line[0].isdigit():

                    roll = [int(item) for item in line.split(",")]

                    self.old_print("roll" + str(roll))

                    self.rolls.append(roll)

    @staticmethod
    def test(path):

        flo = Flo(path)

        game = Game(flo._mock_roller)

        try:
            game.play()
        except SystemExit:
            flo.old_print("no problemo")
        finally:
            flo._exit()

    def _mock_roller(self, num):
        return self.rolls.pop(0)

    def _mock_print(self, *args, **kwargs):

        self.prints += str(*args) + "\n"

    def _mock_input(self, *args, **kwargs):

        self.prints += str(*args)

        response = self.responses.pop(0)

        self.prints += response + "\n"

        return response

    def _exit(self):

        with open(self.path) as file:

            print_lines = self.prints.strip().split("\n")

            file_lines = file.read().strip().split("\n")

            pairs = zip(print_lines, file_lines)

            for i, pair in enumerate(pairs):

                actual, expected = pair

                assert (
                    actual == expected
                ), f"line {i + 1} - actual:{actual} - expected:{expected}"

        builtins.print = self.old_print
        builtins.input = self.old_input


if __name__ == "__main__":
    Flo.test("tests/flow/bank_one_roll_then_quit.txt")
