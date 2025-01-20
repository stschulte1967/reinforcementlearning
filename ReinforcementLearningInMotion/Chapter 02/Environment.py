# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 21:55:57 2023

@author: Stephan Schulte based on Course Reinforcement Leaning in Motion

The Maze class has the following functionality
- Define Maze
- Update Maze
- Returns allowed moves
- check for game over
- Return the state of the system
- Return rewards
- Print maze to terminal

"""
from abc import abstractmethod, ABC
import numpy as np

action_space = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}

class Environment(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update(self, action):
        pass

    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def allowed_moves(self):
        pass

    @abstractmethod
    def is_game_over(self):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def give_reward(self):
        pass

    @abstractmethod
    def is_valid_position(self, position):
        pass


class Maze(Environment):
    def __init__(self):
        self.maze = np.array([[2, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 0, 1],
                     [0, 0, 1, 1, 1, 1],
                     [0, 0, 1, 0, 0, 1],
                     [0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 0]])
        self.state = (0, 0)
        self.target = (5, 5)
        self.steps = 0
        self.allowed_states = {}
        self.construct_allowed_states()

    def update(self, action):
        if action == 'R':
            new_state = (self.state[0], self.state[1] + 1)
        elif action == 'L':
            new_state = (self.state[0], self.state[1] - 1)
        elif action == 'U':
            new_state = (self.state[0] - 1, self.state[1])
        else: #if action == 'D':
            new_state = (self.state[0] + 1, self.state[1])

        self.maze[new_state[0]][new_state[1]] = 2
        self.maze[self.state[0]][self.state[1]] = 0
        self.state = new_state
        self.steps += 1

    def construct_allowed_states(self):
        allowed_states = {}
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if self.maze[y][x] != 1:
                    allowed_states[(y, x)] = []
                    for action in action_space:
                        if self.is_allowed_move((y, x), action):
                            allowed_states[(y, x)].append(action)
        self.allowed_states = allowed_states

    def is_allowed_move(self, state, action):
        y, x = state
        y += action_space[action][0]
        x += action_space[action][1]
        if y < 0 or x < 0 or y > 5 or x > 5:
            return False

        if self.maze[y][x] == 0 or self.maze[y][x] == 2:
            return True
        else:
            return False

    def print(self):
        print("--------")
        for i in range(6):
            line = "|"
            for j in range(6):
                if self.maze[i][j] == 0:
                    line = line + " "
                if self.maze[i][j] == 1:
                    line = line + "X"
                if self.maze[i][j] == 2:
                    line = line + "R"
            print(line + "|")
        print("--------")

    def allowed_moves(self):
        return self.allowed_states[self.state]

    def is_game_over(self):
        if self.state == self.target:
            return True
        return False

    def get_state(self):
        return self.state

    def give_reward(self):
        if self.is_game_over():
            return 0
        else:
            return -1

    def is_valid_position(self, position):
        if 0  <= position[0] <= 5 and 0 <= position[1] <= 5 and 0 == self.maze[position[0]][position[1]]:
            return True
        return False

