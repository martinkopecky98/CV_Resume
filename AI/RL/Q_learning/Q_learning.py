import numpy as np
import gym
import matplotlib.pyplot as plt

pos_space = np.linspace(-1.2, 0.6, 20)
vel_space = np.linspace(-0.07, 0.07, 20)

class Agent():
    def __init__(self, states, action_space = [0,1,2], alpha = 0.1, gamma = 0.99, eps = 0.01, eps_dec = 0.001, eps_min = 0.01):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_dec = eps_dec
        self.eps_min = eps_min
        self.actions = action_space
        self.Q_tab ={}
        for state in states:
            for action in self.actions:
                self.Q_tab[state, action] = 0
    
    def get_state(self, observation):
        pos, vel = observation
        pos_bin = int(np.digitize(pos, pos_space))
        vel_bin = int(np.digitize(vel, vel_space))
        return (pos_bin, vel_bin)

    def max_action(self, state):
        values = np.array([self.Q_tab[state, a] for a in self.actions])
        action = np.argmax(values)
        return action

    def choose_action(self, observation):
        action = np.random.choice(self.actions) if np.random.random() < self.eps else self.max_action(observation)
        self.eps =  self.eps - self.eps_dec if self.eps > self.eps_min else self.eps_min

        return action

    def learn(self, state, action, state_, action_):
        self.Q_tab[state, action] = self.Q_tab[state, action] + self.alpha*(reward + self.gamma*
                                self.Q_tab[state_, action_] - self.Q_tab[state, action] )

env = gym.make("MountainCar-v0")
env._max_episode_steps = 1000

n_games = 500
states = []
for pos in range(21):
    for vel in range(21):
        states.append((pos, vel))

agent = Agent(states, eps_dec=2/n_games)
avg_score = []
total_rewards = np.zeros(n_games)
scores = []
for i in range(n_games):
    done = False
    obs = env.reset()
    state = agent.get_state(obs)
    if i % 100 == 0 and i > 0:
            print('episode ', i, 'score ', score)
    score = 0
    while not done:        
        action = agent.choose_action(state)
        obs_, reward, done, info  = env.step(action)
        state_ = agent.get_state(obs_)
        score += reward
        action_ = agent.max_action(state_)
        agent.learn(state, action, state_, action_)
        state = state_
        score += reward
    scores.append(score)
    avg_score.append(np.average(scores[-100:]))
    total_rewards[i] = score
    log = f'episode: {i} \t score: {score} \t avg_score: {avg_score[i]} \t epsilon: {agent.eps} '
    print(log)
    log = '\n' + log
    with open("notesV2.txt", 'a') as f:
            f.write(log)
mean_n_games = [i for i in range(int(n_games))]

plt.plot(mean_n_games, avg_score)
plt.title('Q-ucenieV3')
plt.savefig('Q-ucenieV3.png')