from Maze import Maze
from Agent import Agent

import matplotlib.pyplot as plt

if __name__ == '__main__':
    maze = Maze()
    robot = Agent(maze, alpha=0.1, epsilon=0.25)
    moveHistory = []
    for i in range(5000):
        if i % 1000 == 0:
            print(i)
        while not maze.isGameOver():
            state, _ = maze.getStateAndReward()
            action = robot.choose_action(state, maze.allowedStates[state])
            maze.updateMaze(action)
            state, reward = maze.getStateAndReward()
            robot.update_memory(state, reward)
            if(maze.steps > 1000):
                maze.state = (5,5)
        robot.train()
        moveHistory.append(maze.steps)
        if i == 4999:
            print(maze.steps)
        maze = Maze()
    maze = Maze()
    robot = Agent(maze, alpha=0.99, epsilon=0.25)
    moveHistory2 = []
    for i in range(5000):
        if i % 1000 == 0:
            print(i)
        while not maze.isGameOver():
            state, _ = maze.getStateAndReward()
            action = robot.choose_action(state, maze.allowedStates[state])
            maze.updateMaze(action)
            state, reward = maze.getStateAndReward()
            robot.update_memory(state, reward)
            if(maze.steps > 1000):
                maze.state= (5,5)
        robot.train()
        moveHistory2.append(maze.steps)
        if i == 4999:
            print(maze.steps)
        maze = Maze()
    
    plt.subplot(211)
    plt.semilogy(moveHistory, 'b--')
    plt.legend(['alpha=0.1'])
    plt.subplot(211)
    plt.semilogy(moveHistory2, 'r--')
    plt.legend(['alpha=0.99'])
    plt.show()