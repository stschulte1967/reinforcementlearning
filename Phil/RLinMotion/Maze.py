import numpy as np

actionSpace = {"UP": (-1,0), "DOWN":(1,0), "RIGHT":(0,1), "LEFT":(0,-1) }

class Maze(object):
    def __init__(self):
        self.maze = np.array( [[2,0,0,0,0,1],
                               [0,0,0,0,0,1],
                               [0,0,1,1,1,0],
                               [0,0,1,0,0,1],
                               [0,0,0,0,0,0],
                               [1,1,1,1,1,0]])
        self.state = (0,0)
        self.steps = 0
        self.constructAllowedStates()
        
        
    def getState(self):
        return self.state
    
    def isDone(self):
        return self.state == (5,5)
    
    def updateMaze(self, action):
        y,x = self.state
        self.maze[self.state] = 0
        y += actionSpace[action][0]
        x += actionSpace[action][1]
        self.state = (y,x)
        self.maze[y,x] = 2
        self.steps += 1
      
            
    def printMaze(self):
        print('_'* 42)
        for row in self.maze:
            for col in self.maze:
                if col == 0:
                    print('', end='\t')
                elif col == 1:
                    print('X', end='\t')
                elif col == 2:
                    print('R', end='\t')
        print('_'* 42)
    
    def isAllowedMove(self, state, action):
        y, x = state
        y += actionSpace[action][0]
        x += actionSpace[action][1]
        if y < 0 or x < 0 or y > 5 or x > 5:
            return False
        if self.maze[y,x] == 0 or self.maze[y,x] == 2:
            return True
        return False
        
    def constructAllowedStates(self):
        allowedStates = {}
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if self.maze[(y,x)] != 1:
                    allowedStates[(y,x)] = []
                    for action in actionSpace:
                        if self.isAllowedMove((y,x), action):
                            allowedStates[(y,x)].append(action)
        self.allowedStates = allowedStates
   
    def isGameOver(self):
        if self.state == (5,5):
            return True
        return False
   
    def getStateAndReward(self):
        reward = self.giveReward()
        return self.state, reward
   
    def giveReward(self):
        if self.state == (5,5):
            return 0
        else:
            return -1
        
    
    
    

    
    
    

