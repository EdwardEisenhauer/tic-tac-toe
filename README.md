# TIC-TAC-TOE

3D 4x4 tic-tac-toe python game, developed to compare heuristic AI algorithms with reinforced learning

## TO DO

 - [ ] verify winning conditions
 - [ ] implement basic reinforced learning
   - [ ] define states (how to define opponents moves?)
   - [ ] define loss
   - [ ] define reward

## Markov Decision Processes

### Assumptions

MDP is a tuple: (_S_,_A_,{_P_sa_},_γ_,_R_), where:

 - _S_ is a set of **states**. In our case a vector (of length 64) which keeps the information about the game-board - if a field is empty, has an **x** or an **o**;

 - _A_ is a set of **actions**. In our case the set of all fields on which agent can place its token (**x** or **o**);

 - _P_sa_ are the state transistion probabilities. It says to what states we will transition if we take action _a_ in state _s_;

 - _γ_∈[0,1) is the **discount factor**;

 - _R_ is the **reward function**.

Our goal in reinforcement learning is to choose actions over time so as to maximize the expected value of the total payoff:

E[R(s0) + γR(s1) + γ^2R(s2) + ...]

A **policy** is any function π:S⟼A.

### Value Iteration



## Important quotes and snippets

### How to teach AI to play Games: Deep Reinforcement Learning - Mauro Comi

https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-learning-28f9b920440a

"Artificial Intelligence and Gaming, contrary to popular belief, do not get along well together. Is this a controversial opinion? Yes, it is, but I’ll explain it. There is a difference between Artificial intelligence and Artificial behavior. We do not want the agents in our games to outsmart players. We want them to be as smart as it’s necessary to provide fun and engagement. We don’t want to push the limit of our ML bot, as we usually do in different Industries. The opponent needs to be imperfect, imitating a human-like behavior."

" No rules about the game are given, and initially the Bot has no information on what it needs to do."

"Reinforcement Learning is an approach based on Markov Decision Process to make decisions."

"Traditional ML algorithms need to be trained with an input and a “correct answer” called target. The system will then try to learn how to predict the target according to new input. In this example, we don’t know what the best action to take at each state of the game is, so a traditional approach would not be effective."

"A Q-table is a matrix, which correlates the state of the agent with the possible actions that the system can adopt."




### Project: Train a AI how to play Snake - maurock

https://github.com/maurock/snake-ga

### CS229 Lecture Notes - Andrew Ng

http://cs229.stanford.edu/notes/cs229-notes12.pdf

"In the reinforcement learning framework, we will instead provide our al-
gorithms only a reward function, which indicates to the learning agent when it is doing well, and when it is doing poorly. (...) It will then be the learning algorithm’s job to figure out how to choose actions over time so as to obtain large rewards."

"Thus, to make this expectation large, we would like to accrue positive rewards as soon as possible (and postpone negative rewards as long as possible)."




