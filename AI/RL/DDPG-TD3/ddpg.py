import os
import numpy as np
import torch as T
import torch.nn.functional as F
import random
from networks import ActorNetwork, CriticNetwork
from noise import OUActionNoise
from buffer import ReplayBuffer

class Agent():
    def __init__(self, input_dims, n_actions, tau = 0.001, gamma=0.99,        
                  batch_size=128, epsilon = 1.0, epsilon_dec = 1e-4, epsilon_min = 0.01,
                  zohriatie = 2000, noise = 0.1):               #funguje namiesto epsilon greedy politiky
        self.gamma = gamma
        self.tau = tau
        self.batch_size = batch_size
        self.n_actions = n_actions
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_dec = epsilon_dec
        self.zohriatie = zohriatie
        self.memory = ReplayBuffer(input_dims, n_actions)

        self.noise = OUActionNoise(mu=np.zeros(n_actions))
        self.steps = 0
        dim = 128
        self.actor = ActorNetwork('actor_ddpg_'+str(dim), input_dims, n_actions, fc1_dims= dim, fc2_dims=dim)
        self.critic = CriticNetwork('critic_ddpg_'+str(dim), input_dims, n_actions, fc1_dims= dim, fc2_dims=dim)
        self.target_actor = ActorNetwork('target_actor_ddpg_'+str(dim), input_dims, n_actions, fc1_dims= dim, fc2_dims=dim)
        self.target_critic = CriticNetwork('target_critic_ddpg_'+str(dim), input_dims, n_actions, fc1_dims= dim, fc2_dims=dim)

        self.update_network_parameters(tau=1)


    def choose_action(self, observation):

        # if self.steps < self.zohriatie: # namiesto toho môžeme aplikovat epsilon greedy politiku
        #     akcia = T.tensor(np.random.normal(0.1, size=(self.n_actions,))).to(self.actor.device)
           
        # if np.random.random() > self.epsilon:
        state = T.tensor([observation], dtype=T.float).to(self.actor.device)    
        mu = self.actor.forward(state).to(self.actor.device)            
        mu_prime = mu + T.tensor(self.noise(),                          
                                    dtype=T.float).to(self.actor.device)
        # mu_prime = mu     # bez noise

        x = mu_prime.cpu().detach().numpy()[0][0]       # treba zmeniť podľa toho koľko akcií v prostredí môžeme vykonať 
        y = mu_prime.cpu().detach().numpy()[0][1]      
        # z = mu_prime.cpu().detach().numpy()[0][2]      
        # w = mu_prime.cpu().detach().numpy()[0][3]      
        # akcia = [x,y,z,w]
        akcia = [x,y]
        # print('bez epsilonu')
        # else:
        #     self.epsilon = max(self.epsilon - self.epsilon_dec, self.epsilon_min)
        #     x = random.uniform(-1.0,1.0)
        #     y = random.uniform(-1.0,1.0)
        #     # z = random.uniform(-1.0,1.0)
        #     # w = random.uniform(-1.0,1.0)
        #     # akcia = [x,y,z,w]  
        #     akcia = [x,y]   
        self.steps += 1
        return akcia

    def remember(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def save_models(self):
        self.actor.save_checkpoint()
        self.target_actor.save_checkpoint()
        self.critic.save_checkpoint()
        self.target_critic.save_checkpoint()

    def load_models(self):
        self.actor.load_checkpoint()
        self.target_actor.load_checkpoint()
        self.critic.load_checkpoint()
        self.target_critic.load_checkpoint()

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        states, actions, rewards, new_states, done = \
                self.memory.sample_buffer(self.batch_size)

        states = T.tensor(states, dtype=T.float).squeeze(1).to(self.actor.device)
        new_states = T.tensor(new_states, dtype=T.float).squeeze(1).to(self.actor.device)
        actions = T.tensor(actions, dtype=T.float).to(self.actor.device)
        rewards = T.tensor(rewards, dtype=T.float).to(self.actor.device)
        done = T.tensor(done).to(self.actor.device)

        target_actions = self.target_actor.forward(new_states)
        target_critic_value_ = self.target_critic.forward(new_states, target_actions)
        critic_value = self.critic.forward(states, actions)

        target_critic_value_[done] = 0.0
        target_critic_value_ = target_critic_value_.view(-1)

        target = rewards + self.gamma*target_critic_value_
        target = target.view(self.batch_size, 1)

        self.critic.optimizer.zero_grad()
        critic_loss = F.mse_loss(target, critic_value)
        critic_loss.backward()
        self.critic.optimizer.step()

        self.actor.optimizer.zero_grad()
        actor_loss = -self.critic.forward(states, self.actor.forward(states))
        actor_loss = T.mean(actor_loss)
        actor_loss.backward()
        self.actor.optimizer.step()
        log = '\nactor_loss: ' + str(actor_loss.data) + '\t\tcritic_loss: ' + str(critic_loss.data)
        with open("Net_loss.txt", 'a') as f:
            f.write(log)
        self.update_network_parameters()

    def update_network_parameters(self, tau=None):
        if tau is None:
            tau = self.tau

        actor_params = self.actor.named_parameters()
        critic_params = self.critic.named_parameters()
        target_actor_params = self.target_actor.named_parameters()
        target_critic_params = self.target_critic.named_parameters()

        critic_state_dict = dict(critic_params)
        actor_state_dict = dict(actor_params)
        target_critic_state_dict = dict(target_critic_params)
        target_actor_state_dict = dict(target_actor_params)

        for name in critic_state_dict:
            critic_state_dict[name] = tau*critic_state_dict[name].clone() + \
                                (1-tau)*target_critic_state_dict[name].clone()

        for name in actor_state_dict:
             actor_state_dict[name] = tau*actor_state_dict[name].clone() + \
                                 (1-tau)*target_actor_state_dict[name].clone()

        