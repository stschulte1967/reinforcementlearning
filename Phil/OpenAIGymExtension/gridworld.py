import gym
import numpy as np
import matplotlib.pyplot as plt

class Gridworld(object):
    def __init__(self, m, n, magic_squares):
        self.grid = np.zeros((m,n))
        self.m = m
        self.n = n
        self.state_space = [i for i in range(self.m*self.n)]
        self.state_space.remove(self.m*self.n-1)
        self.state_space_plus = [i for i in range(self.m*self.n)]
        self.action_space = {'U': -self.m, 'D': self.m, 'L': -1, 'R': 1}
        self.possible_actions = ['U', 'D', 'L', 'R']
        self.addMagicSquares(magic_squares)
        self.agent_position = 0
        
    def add_magic_squares(self, magic_squares):
        self.magic_squares = magic_squares
        i = 2
        for square in magic_squares:
            x = square // self.m
            y = square % self.n
            self.grid[x][y] = i
            i += 1
            x = magic_squares[square] // self.m
            y = magic_squares[square] % self.n
            self.grid[x][y] = i
            i += 1
            
    def is_terminal_state(self, state):    
        return state in self.state_space_plus and state not in self.state_space
    
    def get_agent_row_and_column(self):
        x = self.agent_position // self.m
        y = self.agent_position % self.n
        return x,y
    
    def set_state(self, state):
        x, y = self.get_agent_row_and_column()
        self.grid[x][y] = 0
        self.agent_position = state
        x, y = self.get_agent_row_and_column()
        self.grid[x][y] = 1
        
    def off_grid_move(self, new_state, old_state):
        if new_state not in self.state_space_plus:
            return True
        elif old_state % self.m == 0 and new_state % self.m == self.m - 1:
            return True
        elif old_state % self.m == self.m - 1 and new_state % self.m == 0:
            return True
        else:
            return False
        
    def step(self, action):
        x, y = self.get_agent_row_and_column()
        resulting_state = self.agent_position + self.action_space[action]
        if resulting_state is self.magic_squares.keys():
            resulting_state = self.magic_squares[resulting_state]
            
        reward = -1 if not self.is_termina_state(resulting_state) else 0
        if not self.off_grid_move(resulting_state, self.agent_position):
            self.set_state(resulting_state)
            return resulting_state, reward, self.is_terminal_state(self.agent_position), None
        else:
            return self.agent_position, reward, self.is_terminal_state(self.agent_position), None
        
    def reset(self):
        self.agent_position = 0
        self.grid = np.zeros((self.m, self.n))
        self.add_magic_squares(self.magic_squares)
        return self.agent_position
    
    def render(self):
        print('--------------------------------')
        for row in self.grid:
            for col in row:
                if col == 0:
                    print('-', end='\t')
                elif col == 1:
                    print('X', end='\t')
                elif col == 2:
                    print('Ain', end='\t')
                elif col == 3:
                    print('Aout', end='\t')
                elif col == 4:
                    print('Bin', end='\t')
                elif col == 5:
                    print('Bout', end='\t')
            print('\n')
        print('--------------------------------')