import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import copy
import gym
import os
import datetime
import matplotlib.pyplot as plt
import datetime
import time

class Network(nn.Module):
    def __init__(self, vstup_data, vystup_data, lr = 0.001, fc1_dim = 256, fc2_dim = 256):
        super(Network, self).__init__()

        self.fc1 = nn.Linear(*vstup_data, fc1_dim)
        self.fc2 = nn.Linear(fc1_dim, fc2_dim)
        self.fc3 = nn.Linear(fc2_dim, vystup_data)

        self.loss = nn.MSELoss()
        self.optimizer = optim.Adam(self.parameters(), lr = lr )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def forward(self, stav):
        x = F.relu(self.fc1(stav))
        x = F.relu(self.fc2(x))
        akcia = self.fc3(x)
        return akcia

class Buffer():
    def __init__(self,  state_dim, mem_size = 10_000):
        self.index = 0
        self.mem_size = mem_size
        dimenzia = (mem_size,) + state_dim
        self.state_memory = np.zeros(dimenzia, dtype=np.float32)
        self.action_memory = np.zeros((mem_size), dtype=np.int32)
        self.reward_memory = np.zeros(mem_size,dtype=np.float32)
        self.new_state_memory = np.zeros(dimenzia, dtype=np.float32)
        self.terminal = np.zeros(mem_size, dtype=np.bool)

    def store(self, state, action, reward, new_state, done):
        index = self.index % self.mem_size
        self.state_memory[index] = state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.new_state_memory[index] = new_state
        self.terminal[index] = (done)
        self.index += 1

    def sample(self, batch_size):
        pom = min(self.mem_size, self.index)
        batch = np.random.choice(pom, batch_size, replace= False)
        state = torch.tensor(self.state_memory[batch])
        action = self.action_memory[batch]
        reward = torch.tensor(self.reward_memory[batch])
        new_state = torch.tensor(self.new_state_memory[batch])
        terminal = torch.tensor(self.terminal[batch])
        return state, action, reward, new_state, terminal


class Agent():
    def __init__(self, gamma, state_dim, n_actions, epsilon = 1.0, epsilon_dec = 0.001, epsilon_min = 0.01, update = 1000, batch_size = 64):
        self.buffer = Buffer(state_dim)
        self.gamma = gamma
        self.network = Network(state_dim, n_actions)
        self.target_network = copy.deepcopy(self.network)
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.n_actions = n_actions
        self.update_counter = 0
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.update = update

    def choose_action(self, observation ): # = np.zeros(0)
        random = np.random.random()
        if random < self.epsilon:
            return np.random.choice(self.n_actions)

        state = observation.unsqueeze(0).to(self.device).float()

        actions = self.network.forward(state)
        action = torch.argmax(actions).item()
        return action

    def store_data(self, state, action, reward, new_state, done):
        self.buffer.store(state, action, reward, new_state, done)

    def learn(self):
        if self.buffer.index < 100 :
            return
        self.network.optimizer.zero_grad()
        states, actions, rewards, new_states, terminals = self.buffer.sample(self.batch_size)

        states.to(self.device)
        rewards.to(self.device)
        new_states.to(self.device)
        terminals.to(self.device)

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        q_eval = self.network.forward(states)[batch_index, actions]
        
        #       nepouzivanie target network
        # q_next = self.network.forward(new_states)
        # q_next = self.target_network(new_states.to(self.device)).cpu()
        q_next = self.target_network(new_states)
        
        q_next[terminals] = 0.0
        q_target = rewards + self.gamma * torch.max(q_next, dim = 1)[0]
        loss = self.network.loss(q_target, q_eval).to(self.device)

        loss.backward()
        self.network.optimizer.step()

        self.update_counter += 1
        if self.update_counter % self.update :
            self.target_network.load_state_dict(self.network.state_dict())
        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_dec

env = gym.make("LunarLander-v2")
print(env.action_space.n, env.observation_space.shape )
agent = Agent(0.99, env.observation_space.shape, env.action_space.n)

#       nacitavanie ulozenych parametrov siete
# checkpoint_file = os.path.join("save/", "DQN")
# agent.network.load_state_dict(torch.load(checkpoint_file))
# print("---loadet---")
# torch.load_state_dict('/save/DQN',agent.network.state_dict())

scores = []
avg_score = []
max_score = 0
time = datetime.time
# checkpoint_file = os.path.join('/')
checkpoint_file = os.path.join("save/", "DQN-V4")
d_now = datetime.datetime.now()
n_games = 500
koniec = False
for games in range(n_games):
    score = 0
    done = False
    state = env.reset()
    state = torch.from_numpy(state).double()
    while not done:
        action = agent.choose_action(state)
        new_state, reward, done, _ = env.step(action)
        agent.store_data(state, action, reward, new_state, done)
        state = torch.from_numpy(new_state).double()
        agent.learn()
        score += reward
    if max_score < score :
        max_score = score  
    scores.append(score)
    avg_score.append(np.average(scores[-100:]))
    if games % 50 == 0:
        torch.save(agent.network.state_dict(), checkpoint_file)
    if games % 10 == 0:
        d_end = datetime.datetime.now()
        d = d_end - d_now
        print('time: ', d)
    log = f'episode: {games} \t score: {score} \t avg_score: {avg_score[games]} \t max_score: {max_score}\t epsilon: {agent.epsilon}'
    print(log)
    log = '\n' + log
    
    with open("notesV4.txt", 'a') as f:
        f.write(log)

    
mean_n_games = [i for i in range(int(n_games+1))]
# print(len(mean_n_games), len(avg_score) )
plt.plot(mean_n_games, avg_score)
plt.title('DQN-V1')
plt.savefig('DQN-V4.png')

