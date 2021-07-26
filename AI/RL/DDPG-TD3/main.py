import os
import gym
import numpy as np
import torch as T
import datetime
import matplotlib.pyplot as plt
from ddpg import Agent
from td3 import Agent
from utils import make_env # iba pri cnn a CarRacing

env = gym.make("Pendulum-v0")
# env = gym.make("LunarLanderContinuous-v2")
# env = gym.make('BipedalWalker-v3')
env = make_env('CarRacing-v0') # pouzit td3 agenta a cnn siete
print(env.action_space.shape[0])
agent = Agent(input_dims=env.observation_space.shape, n_actions=env.action_space.shape[0], env = env)
n_games = 2000


best_score = env.reward_range[0]
score_history = []
avg_scores = []
time = datetime.time()

for i in range(n_games):
    observation = env.reset()

    # pri cnn a CarRacing
    # observation = np.array(observation)
    # observation = observation.astype(float)

    done = False
    score = 0
    # agent.noise.reset() #nerobit pri td3
    d_now = datetime.datetime.now()

    while not done:
        action = agent.choose_action(observation)
        observation_, reward, done, info = env.step(action)

        #robit len pri cnn a CarRacing
        # observation_ = np.array(observation_)
        # observation_ = observation_.astype(float)

        score += reward
        agent.remember(observation, action, reward, observation_, done)
        agent.learn()
        observation = observation_
    score_history.append(score)
    avg_score = np.mean(score_history[-100:])
    avg_scores.append(avg_score)

    # if avg_score > best_score:
    #     best_score = avg_score
    #     print('--- ukladanie vysledkov ---')
    #     agent.save_models()

    d_end = datetime.datetime.now()
    d = d_end - d_now
    log = 'episode ' + str(i) +'\t\tscore %.1f ' % score + '\t\taverage score %.1f ' % avg_score + '\t\t time: ' + str(d)
    print(log)
    log = '\n' + log
    # with open("notes.txt", 'a') as f:
    #     f.write(log)

# vykreslovanie grafu. Zmenit nazov a titul podla prostredia a parametrov 
# nazov = 'Pendulum_64x64.png'
# x = [i+1 for i in range(n_games)]
# plt.plot(x, avg_scores)
# plt.title('TD3-64x64/64')
# plt.savefig(nazov)