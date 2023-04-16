import tensorflow as tf
import numpy
import random
import connect4
import training_tools
import copy

inputs:tf.keras.layers.Dense = tf.keras.layers.Input(42)
h1:tf.keras.layers.Dense = tf.keras.layers.Dense(600, "relu", kernel_initializer="random_uniform")
h2:tf.keras.layers.Dense = tf.keras.layers.Dense(500, "relu", kernel_initializer="random_uniform")
h3:tf.keras.layers.Dense = tf.keras.layers.Dense(400, "relu", kernel_initializer="random_uniform")
h4:tf.keras.layers.Dense = tf.keras.layers.Dense(250, "relu", kernel_initializer="random_uniform")
h5:tf.keras.layers.Dense = tf.keras.layers.Dense(150, "relu", kernel_initializer="random_uniform")
h6:tf.keras.layers.Dense = tf.keras.layers.Dense(50, "relu", kernel_initializer="random_uniform")
outputs:tf.keras.layers.Dense = tf.keras.layers.Dense(7, kernel_initializer="random_uniform")

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



# set up
g:connect4.game = connect4.game()
replay_memory = [] # list of experienes from throughout the game
my_turn = True

# variables we will use
illegal_move_disqualification:bool = False

while True:

    # We need to check if the game is over
    need_to_reset = False
    if g.winning():

        if g.winning_for(1):
            print("Game won!")
        else:
            print("Game lost!")

        need_to_reset = True

    elif g.full():
        print("The board is full!")
        need_to_reset = True
    elif illegal_move_disqualification:
        print("Illegal move disqualification!")
        need_to_reset = True
        illegal_move_disqualification = False

    # if there is a need to reset, reset
    if need_to_reset:

        # print the net score
        print ("Score: " + str(training_tools.net_weighted_score(g, 1)))

        print("Resetting... ")
        g = connect4.game()
        replay_memory.clear()
        my_turn = True

    # play the next move!
    if my_turn:

        # measure current net score (will be used later)
        starting_net_score:float = training_tools.net_weighted_score(g, 1)

        # get model outputs
        inputs = numpy.array([g.flatten()])
        outputs = model.predict(inputs, verbose=False)[0]

        # what column are we choosing (what has the highest value)?
        selected_column:int = training_tools.select_column_from_outputs(outputs)

        # execute OUR move
        try:
            g.drop(1, selected_column)
        except:

            # make the experience with a large negative reward because the neural net just tried to make an illegal move, resulting in instantly losing
            exp_d:training_tools.experience = training_tools.experience()
            exp_d.state = g.flatten()
            exp.action = selected_column
            exp.reward = -250.0
            exp.next_state = g.flatten()
            exp.raw_outputs = outputs

            # add to replay memory
            replay_memory.append(exp_d)

            # mark it as disqualified so it is reset next time around
            illegal_move_disqualification = True

    else:

        # execute the opponent's random move
        g.random_move(-1)
        
        # measure the score AFTER our selected move was made and the opponent made his move (in the emulator)
        ending_net_score:float = training_tools.net_weighted_score(g, 1)

        # the change is the reward
        reward:float = ending_net_score - starting_net_score

        # assemble experience
        exp:training_tools.experience = training_tools.experience()
        exp.state = g.flatten()
        exp.action = selected_column
        exp.reward = reward
        exp.next_state = g.flatten()
        exp.raw_outputs = outputs

        # store in replay memory
        replay_memory.append(exp)

        # sample at random from replay memory
        batch = training_tools.random_sample(replay_memory, 0.5)

        # for each experience in the batch
        for old_exp in batch:

            # i need to calculate target (optimal) q value here

            # we have to get the maxq for the FOLLOWING state (the state that follows after this)
            ns_inputs = numpy.array([old_exp.next_state])
            ns_outputs = model.predict(ns_inputs, verbose=False)[0]
            maxqns = max(ns_outputs)

            # calculate target q value
            target_q:float = old_exp.reward + (0.99 * maxqns)

            # set up the data that we will use to perform the backpropogation to "correct" the neural network
            b_inputs = numpy.array([old_exp.state])
            b_optimal_outputs = numpy.array([copy.copy(old_exp.raw_outputs)])
            b_optimal_outputs[0][old_exp.action-1] = target_q
            
            # backpropogate (train)
            model.fit(b_inputs, b_optimal_outputs, verbose=False)
    
    # swap who's turn it is!
    my_turn = not my_turn