import connect4
import enum
import random

# Provides a score for a single player (value)
def weighted_score(g:connect4.game, value:int) -> float:
    
    cumulative_connections:int = g.cummulative_connections(value)
    longest_connect:int = g.longest_connect(value)

    weighted:float = (cumulative_connections * 1.0) + (longest_connect * 50)

    return weighted

# compares a score for the player against the other player. i.e. if the other player did better than you, it is a negative (you did poorly)
def net_weighted_score(g:connect4.game, value:int) -> float:

    my_score:float = weighted_score(g, value)

    if value == 1:
        opponent_score:float = weighted_score(g, -1)
    elif value == -1:
        opponent_score:float = weighted_score(g, 1)
    else:
        raise Exception("I'm not sure what the opponents value should be if your value is not 1 or -1!")

    return my_score - opponent_score

class experience:

    def __init__(self) -> None:

        self.state = [] # board state (flat array)
        self.action:int = 0 # column number that was decided to drop one on (1 through 7)
        self.reward:float = 0.0 # the CHANGE in the net weighted score between the state before and the state aftr my move. (i.e. if I make a bad move and leave a hole open for my opponent, that is a negative reward)
        self.next_state = [] # board state after my move was made (after the opponent's move too)

        self.raw_outputs:list[float] = [] # raw neural network outputs

# Selects the column move decision from neural network 7 outputs
def select_column_from_outputs(outputs) -> int:
    if len(outputs) != 7:
        raise Exception("The number of outputs of this neural network was not 7! Unable to select a column.")
    else:

        chosen_column:int = 1
        on_column = 1

        for v in outputs:
            if v == max(outputs):
                chosen_column = on_column
            on_column = on_column + 1

        return chosen_column
    
# made by GPT-4
def random_sample(lst:list[experience], percentage:float) -> list[experience]:
    k = int(len(lst) * percentage)
    indices = random.sample(range(len(lst)), k)
    return [lst[i] for i in indices]
