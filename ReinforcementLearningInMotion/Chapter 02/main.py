from matplotlib import pyplot as plt
import gymnasium
import stephans_env
from Agent import MazeAgent



if __name__ == '__main__':
    maze = gymnasium.make('stephans_env/MazeWorld-v0')
    agent = MazeAgent(maze, random_factor=0.25, alpha=0.1)
    move_history = []
    episode_over = False

    for i in range(1):
        observation, _ = maze.reset()
        episode_over = False
        steps = 0
        while not episode_over and steps < 5000:
            steps += 1
            state = observation['agent']
            action = agent.choose_action(state)
            observation, reward, terminated, truncated, _ = maze.step(action)
            state = tuple(observation['agent'])
            agent.update_state_history(state, reward)
            episode_over = terminated or truncated
        move_history.append(len(agent.state_history))
        agent.learn()
        print(f"Episode finished in {steps} steps")


    print(move_history[-1])
    plt.subplot(2,1,1)
    plt.plot(move_history, 'b--')
    plt.legend(['alpha=0.1'])
    plt.show()



