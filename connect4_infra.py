import connect4
import enum

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

class move_decision:

    def __init__(self) -> None:

        self.state = []
        self.decision:int = 0 # column number (1 through 7)

class result(enum.Enum):
    loss = 0 # the opponent got 4 in a row
    loss_outscored = 1 # the game wasn't actually lost (the opponent did not get 4 in a row), but they outscored us
    disqualified = 2 # attempt at illegal move was made
    win_outscored = 3 # the game wasn't actually won (we did not get 4 in a row), but we outscored our opponent.
    win = 4 # we got 4 in a row

class game_result:

    def __init__(self) -> None:
        self.move_decisions = []
        self.termination:result = -1 # was it a win, a loss, etc?
        self.net_weighted_score = 0.0