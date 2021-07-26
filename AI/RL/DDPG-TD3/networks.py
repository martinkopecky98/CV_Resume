import os
import numpy as np
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class CriticNetwork(nn.Module):
    def __init__(self, name, input_dims, n_actions,
                beta = 0.001, fc1_dims=256, fc2_dims=256, chkpt_dir='subory/'):
        super(CriticNetwork, self).__init__()
        self.input_dims = input_dims

        self.n_actions = n_actions
        self.name = name 
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name )

        self.fc1 = nn.Linear(*input_dims, fc1_dims) 
        self.fc2 = nn.Linear(fc1_dims, fc2_dims)

        self.action_value = nn.Linear(n_actions, fc2_dims)

        self.q = nn.Linear(fc2_dims, 1)

        self.optimizer = optim.Adam(self.parameters(), beta,
                                    weight_decay=0.01)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state, action):
        state_value = self.fc1(state)
        state_value = F.relu(state_value)
        state_value = self.fc2(state_value)
        action_value = self.action_value(action)
        state_action_value = F.relu(T.add(state_value, action_value))
        state_action_value = self.q(state_action_value)
        return state_action_value

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        file = self.checkpoint_file 
        self.load_state_dict(T.load(file))

    # def load_checkpoint(self,siete):
    #     file = self.checkpoint_file  + '_' + str(siete)
    #     self.load_state_dict(T.load(file))

class ActorNetwork(nn.Module):
    def __init__(self, name, input_dims, n_actions, 
            alpha = 1e-4, fc1_dims= 256, fc2_dims=256, chkpt_dir='subory/'):
        super(ActorNetwork, self).__init__()
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims  
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.name = name
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name )

        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)

        self.mu = nn.Linear(self.fc2_dims, self.n_actions) 

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):  
        
        x = self.fc1(state)
        x = F.relu(x)     
        x = self.fc2(x)
        x = F.relu(x)
        x = T.tanh(self.mu(x))

        return x

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        file = self.checkpoint_file
        self.load_state_dict(T.load(file))

    # def load_checkpoint(self,siete):
    #     file = self.checkpoint_file  + '_' + str(siete)
    #     self.load_state_dict(T.load(file))