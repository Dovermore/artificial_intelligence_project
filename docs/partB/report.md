# Report 

Authors: Chuanyuan Liu, Zhuoqun Huang 

Terminology

* Player vs Agent: Player is generic game concept, where as agent is a concreet implementation of Player.



## Rotate board

Intuition: 

- Players differ by their orintation on the board and this is encoding using the `colour` variable. 
- We can reduce the number of possible states if we assume all players to have the same orientation.
- Orientation of the board does not affect a player's decision, therefore we can safely fix all players to the same orientation. 
- We still need the `colour` variable because it dictates which player moves next. Order of play can affect a player's decision. For example when players mirrors each other's actions, the player who moves first will win the game or draw but cannot lose the game.

Implementation:

1. All agents are assigned the colour red. 
2. Agents 




## Random Agent
We define a random agent as an agent that selects an action that will result in randomly selected state out of uniformly distributed all possible states.

Since distinct move will result in distinct states, the random agent will only need to consider actions.

**Pseudocode code**
```text
1. Input a game state
2. Generate all possible action
3. Use the predefined rules to find valid action 
3. Chose 1 move out of all the valid action. 
```

**Test cases**

1. Test pass 
2. Test all possible valid moves





## Max N Agent

What is a good depth to choose? 

In the first iteration we limited the depth of the search to 5. 

An agent don't need to use MaxN or any evaluation function when it can only carry out a single action. Evaluation functions are only useful when there is a choice between actions. To make the program more efficient we can limit the number of possible actions by reacting immediately to danger much as the possibility of beening eaten. We can also limit the size of the board just like how human chess players spend their attension focusing on the the part of the  chess board with the highest conflict.



## Evaluator

Factors that have positive correlation with winning. Weighting will be asigned using machine learning

Number of pieces:

* Player jump over other player when possible
* Player will avoid other players

Number of exited pieces

* Player would want to exit as soon as possible

Distance to exit

* Player move closer to goal
* Pieces will jump over each other



## Ordering

1. Exit
2. Jump
3. Move



## Test states

#### min_branch_factor.json

* Each player has 1 piece at the corner of the board so the branching factor for each player is the minimum 3. 
* Each piece can only  MOVE and is not in the correct position to EXIT.

### Simple

* 1 piece for each players are in their appropriate exit position. This means a smart agent should try to exit immediately.