# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 21:48:00 2023

@author: Stephan Schulte based on Course Reforcement Leaning in Motion

An Agent has has the following properties:
    - it has to be able to learn from its actions
    - it has to have some type of memory
    - it needs a way to correlate actions/state and rewards
    - it needs some mechanism to choose an action

"""

import numpy as np
from abc import abstractmethod, ABC


action_space = {0: (1,0), 1: (0,-1), 2: (-1,0), 3:(0,1)}

class Agent(ABC):
    @abstractmethod
    def __init__(self, states, alpha, random_factor):
        pass

    @abstractmethod
    def choose_action(self, state):
        pass

    @abstractmethod
    def learn(self):
        pass


class MazeAgent(Agent):
    def __init__(self, env, alpha=0.9, random_factor = 0.2):
        super().__init__(env, alpha, random_factor)
        self.state_history = [((0,0), 0)]
        self.alpha = alpha
        self.G = {}
        self.random_factor = random_factor
        self.init_reward(env)
        self.env = env

    def init_reward(self, env):
        for x in range(6):
            for y in range(6):
                self.G[(x, y)] = np.random.uniform(low=-1.0, high=-0.1)
        print(self.G)

    def choose_action(self, state):
        max_g = -10e15
        next_move = None
        random_n = np.random.random()
        if random_n < self.random_factor:
            next_move = np.random.randint(0,self.env.action_space.n)
        else:
            for action in  action_space:
                new_state = tuple([sum(x) for x in zip(state,action_space[action])])
                if 0 <= new_state[0] <= 5 and 0 <= new_state[1] <= 5 and self.G[new_state] >= max_g:
                    next_move = action
                    max_g = self.G[new_state]
        return next_move

    def learn(self):
        target = 0
        print("state_history", self.state_history)
        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] +  self.alpha * (target - self.G[prev])
            target += reward
            print(prev, reward, target, self.G[prev])
        print(target,self.G)
        self.state_history = []
        self.random_factor -= 10e-5


    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))
