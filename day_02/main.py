"""
--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach.
To decide whose tent gets to be closest to the snack storage,
a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players.
Each game contains many rounds;
in each round, the players each simultaneously choose
one of Rock, Paper, or Scissors using a hand shape.
Then, a winner for that round is selected:
Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday,
one Elf gives you an encrypted strategy guide (your puzzle input)
that they say will be sure to help you win.
"The first column is what your opponent is going to play:
A for Rock, B for Paper, and C for Scissors.
The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response:
X for Rock, Y for Paper, and Z for Scissors.
Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score.
Your total score is the sum of your scores for each round.
The score for a single round is the score for the shape you selected
(1 for Rock, 2 for Paper, and 3 for Scissors)
plus the score for the outcome of the round
(0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you,
you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should choose Paper (Y).
    This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
    In the second round, your opponent will choose Paper (B), and you should choose Rock (X).
    This ends in a loss for you with a score of 1 (1 + 0).
    The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide,
you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

--- Part Two ---

The Elf finishes helping with the tent and sneaks back over to you.
"Anyway, the second column says how the round needs to end: X means you need to lose,
Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way,
but now you need to figure out what shape to choose so the round ends as indicated.
The example above now goes like this:

    * In the first round, your opponent will choose Rock (A),
    and you need the round to end in a draw (Y), so you also choose Rock.
    This gives you a score of 1 + 3 = 4.
    * In the second round, your opponent will choose Paper (B),
    and you choose Rock, so you lose (X) with a score of 1 + 0 = 1.
    * In the third round,
    you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.

Now that you're correctly decrypting the ultra top secret strategy guide,
you would get a total score of 12.

Following the Elf's instructions for the second column,
what would your total score be if everything goes exactly according to your strategy guide?
"""
from common import get_input_data


class RockPaperScissorsGame:
    SHAPES = (
        "Rock",
        "Paper",
        "Scissors",
    )

    FIRST_THROWS = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissors",
    }
    SECOND_THROWS_SUPPOSED = {
        "X": "Rock",
        "Y": "Paper",
        "Z": "Scissors",
    }
    SECOND_THROWS_EXPECTED = {
        "X": "Loss",
        "Y": "Draw",
        "Z": "Win",
    }

    THROWS_TO_WIN = {
        "Rock":     "Paper",
        "Paper":    "Scissors",
        "Scissors": "Rock",
    }
    THROWS_TO_LOSE = {
        "Rock":     "Scissors",
        "Paper":    "Rock",
        "Scissors": "Paper",
    }

    SCORES = {
        "Rock":     1,
        "Paper":    2,
        "Scissors": 3,

        "Loss":     0,
        "Draw":     3,
        "Win":      6,
    }

    def __init__(self, input_data: list[str]):
        self.input_data = [line.split(" ") for line in input_data]

    def calculate_scores_supposed(self,
                                  first_throw_code: str,
                                  second_throw_code: str) -> int:
        results = self.SCORES[
            self.SECOND_THROWS_SUPPOSED[second_throw_code]
        ]

        if self.SECOND_THROWS_SUPPOSED[second_throw_code] == \
                self.THROWS_TO_LOSE[self.FIRST_THROWS[first_throw_code]]:
            results += self.SCORES["Loss"]
        elif self.SECOND_THROWS_SUPPOSED[second_throw_code] == \
                self.FIRST_THROWS[first_throw_code]:
            results += self.SCORES["Draw"]
        elif self.SECOND_THROWS_SUPPOSED[second_throw_code] == \
                self.THROWS_TO_WIN[self.FIRST_THROWS[first_throw_code]]:
            results += self.SCORES["Win"]

        return results

    def calculate_scores_expected(self,
                                  first_throw_code: str, 
                                  second_throw_code: str) -> int:
        results = 0

        match self.SECOND_THROWS_EXPECTED[second_throw_code]:
            case "Loss":
                results += self.SCORES[self.THROWS_TO_LOSE[
                    self.FIRST_THROWS[first_throw_code]]
                ]
                results += self.SCORES["Loss"]
            case "Draw":
                results += self.SCORES[self.FIRST_THROWS[
                    first_throw_code]
                ]
                results += self.SCORES["Draw"]
            case "Win":
                results += self.SCORES[self.THROWS_TO_WIN[
                    self.FIRST_THROWS[first_throw_code]]
                ]
                results += self.SCORES["Win"]

        return results

    def calculate_scores(self, keyword: str):
        method = getattr(self, f"calculate_scores_{keyword}")
        return sum([method(*throws) for throws in self.input_data])


if __name__ == "__main__":
    test_game = RockPaperScissorsGame(get_input_data("test_data.txt"))
    prod_game = RockPaperScissorsGame(get_input_data("prod_data.txt"))

    # Part 1
    test_scores_supposed = test_game.calculate_scores("supposed")
    assert test_scores_supposed == 15
    prod_scores_supposed = prod_game.calculate_scores("supposed")
    print(prod_scores_supposed)

    # Part 2
    test_scores_expected = test_game.calculate_scores("expected")
    assert test_scores_expected == 12
    prod_scores_expected = prod_game.calculate_scores("expected")
    print(prod_scores_expected)
