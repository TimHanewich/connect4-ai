import tensorflow as tf
import numpy
import random
import connect4
import connect4_infra

inputs:tf.keras.layers.Dense = tf.keras.layers.Input(42)
h1:tf.keras.layers.Dense = tf.keras.layers.Dense(600, "relu")
h2:tf.keras.layers.Dense = tf.keras.layers.Dense(500, "relu")
h3:tf.keras.layers.Dense = tf.keras.layers.Dense(400, "relu")
h4:tf.keras.layers.Dense = tf.keras.layers.Dense(250, "relu")
h5:tf.keras.layers.Dense = tf.keras.layers.Dense(150, "relu")
h6:tf.keras.layers.Dense = tf.keras.layers.Dense(50, "relu")
outputs:tf.keras.layers.Dense = tf.keras.layers.Dense(7)

model = tf.keras.Sequential()
model.add(inputs)
model.add(h1)
model.add(h2)
model.add(h3)
model.add(h4)
model.add(h5)
model.add(h6)
model.add(outputs)

model.compile("adam", "mean_squared_error")




def decide_next_move(g:connect4.game, m:tf.keras.Sequential) -> connect4_infra.move_decision:

    ToReturn:connect4_infra.move_decision = connect4_infra.move_decision()
    ToReturn.state = g.flatten()

    i = numpy.array([g.flatten()])
    o = model.predict(i, verbose=False)[0]

    # select the chosen column (highest value)
    chosen_column:int = 1
    on_column = 1
    for v in o:
        if v == max(o):
            chosen_column = on_column
        on_column = on_column + 1

    ToReturn.decision = chosen_column
    
    return ToReturn

# always plays value 1 (goes first)
def play_to_completion(g:connect4.game, m:tf.keras.Sequential) -> connect4_infra.game_result:


    ToReturn:connect4_infra.game_result = connect4_infra.game_result()
    my_turn:bool = True # whose turn it is (flips)

    while True:


        # check if the board is full
        board_full = g.full()
        if board_full: # it is game over! board full!

            # score
            net:float = connect4_infra.net_weighted_score(g, 1)
            ToReturn.net_weighted_score = net

            # How did the game terminate?
            if g.winning_for(1): # did I win (connect 4 in a row)?
                ToReturn.termination = connect4_infra.result.win
            elif g.winning_for(-1): # did my opponent win (connect 4 in a row)?
                ToReturn.termination = connect4_infra.result.loss
            else: # if neither of us won by connecting 4, who won by points?
                if net > 0.0:
                    ToReturn.termination = connect4_infra.result.win_outscored
                else:
                    ToReturn.termination = connect4_infra.result.loss_outscored

            # return
            return ToReturn

        if my_turn: # it is my turn, so use the neural network to predict next move and play it

            # play the next move
            next_move:connect4_infra.move_decision = decide_next_move(g, m)

            # store it in the history log
            ToReturn.move_decisions.append(next_move)

            # attempt to play it
            try:
                g.drop(1, next_move.decision)
            except: # if it failed, it is because the move is illegal. So mark it as such and return
                ToReturn.termination = connect4_infra.result.disqualified
                ToReturn.net_weighted_score = connect4_infra.net_weighted_score(g, 1)
                return ToReturn
            
        else: # it is my opponents turn, so play at random (for now)

            # play random move
            g.random_move(-1)

        # before going to the next loop, be sure to flip whose turn it is now!!
        my_turn = not my_turn


# TRAIN!
while True:

    # play 20 games
    game_results = []
    for x in range(20):
        g:connect4.game = connect4.game()
        print("Simulating game # " + str(x+1) + "... ", end="")
        game_result:connect4_infra.game_result = play_to_completion(g, model)
        print(str(game_result.termination))
        game_results.append(game_result)


    # select the best game

    # first, make a list of those that were won or lost at least LEGALLY. And NOT loss by disqualification (illegal move)
    prime_games_to_choose_from = []
    for game_result in game_results:
        if game_result.termination != connect4_infra.result.disqualified:
            prime_games_to_choose_from.append(game_result)

    # if we have no prime games to choose from (none were won or lost legally, add them all in)
    if len(prime_games_to_choose_from) == 0:
        for game_result in game_results:
            prime_games_to_choose_from.append(game_result)

    # select the best out of this bunch
    best_game:connect4_infra.game_result = prime_games_to_choose_from[0]
    for game_result in prime_games_to_choose_from:
        if game_result.net_weighted_score > best_game.net_weighted_score:
            best_game = game_result

    # print some details about the best game
    print("Highest score: " + str(best_game.net_weighted_score) + " (" + str(best_game.termination) + ")")

    # train on that game
    x_train = []
    y_train = []
    for md in best_game.move_decisions:
        md:connect4_infra.move_decision

        # append to x train
        x_train.append(md.state)

        # append to y train
        y_data = [0, 0, 0, 0, 0, 0, 0]
        y_data[md.decision-1] = 1
        y_train.append(y_data)

    # train
    _x_train = numpy.array(x_train)
    _y_train = numpy.array(y_train)
    print("Training... ", end="")
    model.fit(_x_train, _y_train, epochs=50, verbose=False)
    print("Complete!")




        
