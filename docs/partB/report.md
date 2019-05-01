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