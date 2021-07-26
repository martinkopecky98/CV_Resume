import os
import torch as T
import torch.nn.functional as F
import numpy as np
from buffer import ReplayBuffer
from networks import ActorNetwork, CriticNetwork
# from cnn_net import ActorNetwork, CriticNetwork # iba pri cnn a CarRacing

class Agent():
    def __init__(self, input_dims, env, tau = 0.001, alpha = 0.001,
            beta = 0.001, gamma=0.99, update_actor_interval=2, zohriatie=2000, #warmup funguje namiesto epsilon greedy politiky
            n_actions=2, max_size=5_000, fc_dims = 256, batch_size=128, noise=0.1):
        self.gamma = gamma
        self.tau = tau
        self.max_action = env.action_space.high
        self.min_action = env.action_space.low
        self.memory = ReplayBuffer(input_dims, n_actions, max_size)
        self.batch_size = batch_size
        self.learn_step_cntr = 0
        self.time_step = 0
        self.zohriatie = zohriatie
        self.n_actions = n_actions
        self.update_actor_iter = update_actor_interval
        self.noise = noise


        # self.actor = ActorNetwork("actor_td3", input_dims, n_actions, alpha, fc_dims, fc_dims)
        # self.target_actor = ActorNetwork("target_actor_td3", input_dims, n_actions, alpha, fc_dims, fc_dims)
        # self.critic_1 = CriticNetwork('critic_1_td3', input_dims, n_actions, beta, fc_dims, fc_dims)
        # self.critic_2 = CriticNetwork('critic_2_td3', input_dims, n_actions, beta, fc_dims, fc_dims)
        # self.target_critic_1 = CriticNetwork('target_critic_1_td3', input_dims, n_actions, beta, fc_dims, fc_dims)
        # self.target_critic_2 = CriticNetwork('target_critic_2_td3', input_dims, n_actions, beta, fc_dims, fc_dims)
 
        self.actor = ActorNetwork("actor_td3", a, n_actions, alpha, fc_dims, fc_dims)
        self.target_actor = ActorNetwork("target_actor_td3", a, n_actions, alpha, fc_dims, fc_dims)
        self.critic_1 = CriticNetwork('critic_1_td3', b, n_actions, beta, fc_dims, fc_dims)
        self.critic_2 = CriticNetwork('critic_2_td3', b, n_actions, beta, fc_dims, fc_dims)
        self.target_critic_1 = CriticNetwork('target_critic_1_td3', b, n_actions, beta, fc_dims, fc_dims)
        self.target_critic_2 = CriticNetwork('target_critic_2_td3', b, n_actions, beta, fc_dims, fc_dims)

        #siete pri cnn a CarRacing
        # self.actor = ActorNetwork("actor", input_dims, n_actions, alpha, fc_dims)
        # self.target_actor = ActorNetwork("target_actor", input_dims, n_actions, alpha, fc_dims)
        # self.critic_1 = CriticNetwork('critic_1', input_dims, n_actions, beta, fc_dims)
        # self.critic_2 = CriticNetwork('critic_2', input_dims, n_actions, beta, fc_dims)
        # self.target_critic_1 = CriticNetwork('target_critic_1', input_dims, n_actions, beta, fc_dims)
        # self.target_critic_2 = CriticNetwork('target_critic_2', input_dims, n_actions, beta, fc_dims)
       
        self.update_network_parameters(tau=1)

    def choose_action(self, observation):
        if self.time_step < self.zohriatie: # namiesto toho môžeme aplikovat epsilon greedy politiku
            mu = T.tensor(np.random.normal(scale=self.noise, size=(self.n_actions,))).to(self.actor.device)
        else:
            state = T.tensor(observation, dtype=T.float).unsqueeze_(0).to(self.actor.device)
            mu = self.actor.forward(state).to(self.actor.device).squeeze(0)
            print('za zohrevanim')
        mu_prime = mu + T.tensor(np.random.normal(scale=self.noise),
                dtype=T.float).to(self.actor.device)
        mu_prime = T.clamp(mu_prime, self.min_action[0], self.max_action[0])
        self.time_step += 1
        return mu_prime.cpu().detach().numpy()

    def remember(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        state, action, reward, new_state, done = \
                self.memory.sample_buffer(self.batch_size)

        reward = T.tensor(reward, dtype=T.float).to(self.critic_1.device)
        done = T.tensor(done).to(self.critic_1.device)
        state_ = T.tensor(new_state, dtype=T.float).to(self.critic_1.device)
        state = T.tensor(state, dtype=T.float).to(self.critic_1.device)
        action = T.tensor(action, dtype=T.float).to(self.critic_1.device)

        target_actions = self.target_actor.forward(state_)
        target_actions = target_actions + \
                T.clamp(T.tensor(np.random.normal(scale=0.2)), -0.5, 0.5)
        target_actions = T.clamp(target_actions, self.min_action[0], self.max_action[0])

        q1_ = self.target_critic_1.forward(state_, target_actions)
        q2_ = self.target_critic_2.forward(state_, target_actions)

        q1 = self.critic_1.forward(state, action)
        q2 = self.critic_2.forward(state, action)

        q1_[done] = 0.0
        q2_[done] = 0.0

        q1_ = q1_.view(-1)
        q2_ = q2_.view(-1)

        critic_value_ = T.min(q1_, q2_)

        target = reward + self.gamma*critic_value_
        target = target.view(self.batch_size, 1)

        self.critic_1.optimizer.zero_grad()
        self.critic_2.optimizer.zero_grad()

        q1_loss = F.mse_loss(target, q1)
        q2_loss = F.mse_loss(target, q2)
        critic_loss = q1_loss + q2_loss
        critic_loss.backward()

        self.critic_1.optimizer.step()
        self.critic_2.optimizer.step()

        self.learn_step_cntr += 1

        if self.learn_step_cntr % self.update_actor_iter != 0:
            return

        self.actor.optimizer.zero_grad()
        actor_q1_loss = self.critic_1.forward(state, self.actor.forward(state))
        actor_loss = -T.mean(actor_q1_loss)
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
        critic_1_params = self.critic_1.named_parameters()
        critic_2_params = self.critic_2.named_parameters()
        target_actor_params = self.target_actor.named_parameters()
        target_critic_1_params = self.target_critic_1.named_parameters()
        target_critic_2_params = self.target_critic_2.named_parameters()

        critic_1_state_dict = dict(critic_1_params)
        critic_2_state_dict = dict(critic_2_params)
        actor_state_dict = dict(actor_params)
        target_actor_state_dict = dict(target_actor_params)
        target_critic_1_state_dict = dict(target_critic_1_params)
        target_critic_2_state_dict = dict(target_critic_2_params)

        for name in critic_1_state_dict:
            critic_1_state_dict[name] = tau*critic_1_state_dict[name].clone() + \
                    (1-tau)*target_critic_1_state_dict[name].clone()

        for name in critic_2_state_dict:
            critic_2_state_dict[name] = tau*critic_2_state_dict[name].clone() + \
                    (1-tau)*target_critic_2_state_dict[name].clone()

        for name in actor_state_dict:
            actor_state_dict[name] = tau*actor_state_dict[name].clone() + \
                    (1-tau)*target_actor_state_dict[name].clone()

        self.target_critic_1.load_state_dict(critic_1_state_dict)
        self.target_critic_2.load_state_dict(critic_2_state_dict)
        self.target_actor.load_state_dict(actor_state_dict)

    def save_models(self):
        self.actor.save_checkpoint()
        self.target_actor.save_checkpoint()
        self.critic_1.save_checkpoint()
        self.critic_2.save_checkpoint()
        self.target_critic_1.save_checkpoint()
        self.target_critic_2.save_checkpoint()

    def load_models(self):
        self.actor.load_checkpoint()
        self.target_actor.load_checkpoint()
        self.critic_1.load_checkpoint()
        self.critic_2.load_checkpoint()
        self.target_critic_1.load_checkpoint()
        self.target_critic_2.load_checkpoint()

    def load_models(self,siete):
        self.actor.load_checkpoint(siete)
        self.target_actor.load_checkpoint(siete)
        self.critic_1.load_checkpoint(siete)
        self.critic_2.load_checkpoint(siete)
        self.target_critic_1.load_checkpoint(siete)
        self.target_critic_2.load_checkpoint(siete)

    def save_models_check(self, path, i):
        self.actor.save_checkpoint_check(path, i)
        self.target_actor.save_checkpoint_check(path, i)
        self.critic_1.save_checkpoint_check(path, i)
        self.critic_2.save_checkpoint_check(path, i)
        self.target_critic_1.save_checkpoint_check(path, i)
        self.target_critic_2.save_checkpoint_check(path, i)