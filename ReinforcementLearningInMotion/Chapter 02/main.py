from matplotlib import pyplot as plt

from Agent import MazeAgent
from Environment import Maze

if __name__ == '__main__':
    maze = Maze()
    agent = MazeAgent(maze, random_factor=0.25, alpha=0.1)
    move_history = []

    for i in range(5000):
        while not maze.is_game_over():
            state = maze.get_state()
            action = agent.choose_action(state, maze.allowed_moves())
            maze.update(action)
            state = maze.get_state()
            reward = maze.give_reward()
            agent.update_state_history(state, reward)
            if maze.steps > 1000:
                maze.state = (5,5)
        agent.learn()
        move_history.append(maze.steps)
        maze = Maze()
    print(move_history[-1])


    maze = Maze()
    agent2 = MazeAgent(maze, random_factor=0.25, alpha=0.99)
    move_history2 = []

    for i in range(5000):
        while not maze.is_game_over():
            state = maze.get_state()
            action = agent2.choose_action(state, maze.allowed_moves())
            maze.update(action)
            state = maze.get_state()
            reward = maze.give_reward()
            agent2.update_state_history(state, reward)
            if maze.steps > 1000:
                maze.state = (5, 5)
        agent2.learn()
        move_history2.append(maze.steps)
        maze = Maze()
    print(move_history[-1])
    plt.subplot(2,1,1)
    plt.plot(move_history, 'b--')
    plt.legend(['alpha=0.1'])
    plt.subplot(2,1,2)
    plt.plot(move_history2)
    plt.legend(['alpha=0.99'])
    plt.show()



