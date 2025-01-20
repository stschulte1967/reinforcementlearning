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

action_space = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R':(0,1)}

class Agent(ABC):
    @abstractmethod
    def __init__(self, states, alpha, random_factor):
        pass


    @abstractmethod
    def choose_action(self, state, allowed_moves):
        pass

    @abstractmethod
    def learn(self):
        pass

    @abstractmethod
    def update_state_history(self, state, reward):
        pass


class MazeAgent(Agent):
    def __init__(self, env, alpha=0.9, random_factor = 0.2):
        super().__init__(env, alpha, random_factor)
        self.state_history = [((0,0), 0)]
        self.alpha = alpha
        self.G = {}
        self.random_factor = random_factor
        self.init_reward(env.allowed_states)

    def init_reward(self, states):
        for state in states:
            self.G[state] = np.random.uniform(low=-1.0, high=-0.1)

    def choose_action(self, state, allowed_moves):
        max_g = -10e15
        next_move = None
        random_n = np.random.random()
        if random_n < self.random_factor:
            next_move = np.random.choice(allowed_moves)
        else:
            for action in allowed_moves:
                new_state = tuple([sum(x) for x in zip(state, action_space[action])])
                if self.G[new_state] >= max_g:
                    next_move = action
                    max_g = self.G[new_state]
        return next_move

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] +  self.alpha * (target - self.G[prev])
            target += reward
        self.state_history = []
        self.random_factor -= 10e-5


    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))
