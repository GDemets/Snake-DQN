# Snake-DQN

:warning: **WORK IN PROGRESS** :warning:

## First results

## Some problems

### Bad Results
At the beginning with the bad parameters the results was pretty bad. 
![til](../Snake-DQN/img/output_config1.png)
With over 3 000 trials the models perform with under 0.5 of score per game, which is pretty bad. 

### Infinite boucle
Another issue discover during this project, sometimes with my seconde configuration the agent just go in a infinite boucle. To avoid this nehaviour we can add a condition that after 200 steps the game is over and receive a punition. 
![til](../Snake-DQN/img/Infinite_boucle.gif)

## Final results

## Ressources
- https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
- https://docs.pytorch.org/tutorials/advanced/pendulum.html
- https://docs.pytorch.org/tutorials/intermediate/mario_rl_tutorial.html
- https://cs229.stanford.edu/proj2016spr/report/060.pdf
- https://arxiv.org/pdf/1509.06461
