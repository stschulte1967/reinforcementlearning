import gym
import numpy as np
from gym import wrappers
import matplotlib.pyplot as plt

env = gym.make('CartPole-v0')

max_states = 10 ** 4
gamma = 0.9
alpha = 0.01


def max_dict(d):
    max_v = float('-inf')
    for key, val in d.items():
        if val > max_v:
            max_v = val
            max_key = key
    return max_key, max_v


def create_bins():
    bins = np.zeros((4, 10))
    bins[0] = np.linspace(-4.8, 4.8, 10)
    bins[1] = np.linspace(-5, 5, 10)
    bins[2] = np.linspace(-0.418, 0.418, 10)
    bins[3] = np.linspace(-5, 5, 10)
    return bins


def assign_bins(observation, bins):
    state = np.zeros(4)
    for i in range(4):
        state[i] = np.digitize(observation[i], bins[i])
    return state


def get_state_as_string(state):
    string_state = ''.join(str(int(e)) for e in state)
    return string_state


def get_all_states_as_string():
    states = []
    for i in range(max_states):
        states.append(str(i).zfill(4))
    return states


def initialize_q():
    q = {}
    all_states = get_all_states_as_string()
    for state in all_states:
        q[state] = {}
        for action in range(env.action_space.n):
            q[state][action] = 0
    return q

def play_one_game(bins, q, eps=0.5):
    observation = env.reset()
    done = False
    cnt = 0
    state = get_state_as_string(assign_bins(observation, bins))
    total_reward = 0

    while not done:
        cnt += 1

        if np.random.uniform() < eps:
            act = env.action_space.sample()
        else:
            act = max_dict(q[state])[0]

        observation, reward, done, _ = env.step(act)

        total_reward += reward

        if done and cnt < 200:
            reward = -300

        state_new = get_state_as_string(assign_bins(observation, bins))
        a1, max_q_slal = max_dict(q[state_new])
        q[state][act] += alpha * (reward + gamma * max_q_slal - q[state][act])
        state, act = state_new, a1
    return total_reward, cnt


def play_many_games(bins, N=10000):
    q = initialize_q()
    length = []
    reward = []
    for n in range(N):
        eps = 1.0 / np.sqrt(n+1)
        episode_reward, episode_length = play_one_game(bins, q, eps)
        if n % 100 == 0:
            print(n, '%.4f' % eps, episode_reward)
        length.append(episode_length)
        reward.append(episode_reward)
    return length, reward


def plot_running_avg(total_rewards):
    N = len(total_rewards)
    running_avg = np.empty(N)
    for t in range(N):
        running_avg[t] = np.mean(total_rewards[max(0, t-100):(t+1)])
    plt.plot(running_avg)
    plt.title("Running Average")
    plt.show()


if __name__ == '__main__':
    bins = create_bins()
    episode_length, episode_rewards = play_many_games(bins)

    plot_running_avg(episode_rewards)
