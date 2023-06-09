## Game Process (from 6:28 in https://youtu.be/0bt0SjbS3xc)
1. Initialize replay memory capacity.
2. Initialize network with random weights.
3. *For each episode*:
    1. Initialize the starting state.
    2. *For each time step*:
        1. Select an action. (via exploration or exploitation)
        2. Execute selected action in an emulator.
        3. Observe reward and next state.
        4. Store experience in replay memory.
        5. Sample random batch from replay memory.
        6. Preprocess states from batch (prepare to pass through neural network).
        7. Pass batch of preprocessed states to policy network.
        8. For each experience in the batch, calculate loss between output Q-values and target (optimal) Q-values.
            - Doing this *will* require a second pass through the network for the next state.
        9. Gradient descent updates weightes in the policy network to minimize loss (backpropogate/train network).

## Target (Optimal Q) Equation
Taken from https://youtu.be/0bt0SjbS3xc?t=269 at 4:29  
![target q](./target_q.png)
- **Rt+1** is the reward at this time step.
- **The gamma (y looking thing)** is the discount factor. Use 0.99.
- **maxq(s1,a1)** is the highest q value output out of any of the values outputted from the network for the NEXT state action pair that is for the state that occurs AFTER the action in this time step is chosen.