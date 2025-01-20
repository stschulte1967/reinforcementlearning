import numpy as np

class Agent(object):
    def __init__(self, maze, alpha=0.15, epsilon=0.2):
        self.memory = [((0,0), 0)]
        self.alpha = alpha
        self.G = {}
        self.initReward(maze.allowedStates)
        self.actionSpace = {"UP": (-1,0), "DOWN":(1,0), "RIGHT":(0,1), "LEFT":(0,-1) }
        self.epsilon = epsilon
    
    def initReward(self, states):
        for state in states:
            self.G[state] = np.random.uniform(low=-1.0, high=-0.1)
    
    def train(self):
        target = 0
        for prev, reward in reversed(self.memory):
            self.G[prev] += self.alpha * (target - self.G[prev])
            target += reward
        self.memory = []
        self.epsilon -= 10e-5
        
    def choose_action(self, state, allowedMoves):
        maxG = -10e15
        nextMove=None
        randomN = np.random.random()
        if randomN < self.epsilon:
            nextMove = np.random.choice(allowedMoves)
        else:
            for action in allowedMoves:
                newState = tuple([sum(x) for x in zip(state, self.actionSpace[action])])
                if self.G[newState] >= maxG:
                    nextMove = action
                    maxG     = self.G[newState]
        return nextMove
        
    
    def update_memory(self, state, reward):
        self.memory.append((state, reward))
    
