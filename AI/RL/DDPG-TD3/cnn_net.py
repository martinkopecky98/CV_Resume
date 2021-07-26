import os
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


cnn_base = nn.Sequential(
    nn.Conv2d(in_channels=4, out_channels=32, kernel_size=3, stride=2, padding=1), #32,48,48
    nn.ReLU(),
    nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=2, padding=1), #64,24,24
    nn.ReLU(),
    nn.Conv2d(in_channels=64, out_channels=32, kernel_size=3, stride=2, padding=1), #32,12,12
    nn.ReLU(),
    nn.Conv2d(in_channels=32, out_channels=16, kernel_size=3, stride=2, padding=1), #16,6,6 /
    nn.ReLU(),
    nn.Flatten(start_dim=1)
).to(T.device('cuda:0' if T.cuda.is_available() else 'cpu'))


class CriticNetwork(nn.Module):
    def __init__(self, name, input_dims, n_actions,
             beta = 0.001, fc_dims = 256,  chkpt_dir='subory/'):
        super(CriticNetwork, self).__init__()
        self.input_dims = input_dims
        self.n_actions = n_actions
        self.name = name
        self.checkpoint_file = os.path.join(chkpt_dir, name+'_td3')

        self.fc1 = nn.Linear(576 + n_actions, fc_dims)
        self.q1 = nn.Linear(fc_dims, 1)
        self.action_value = nn.Linear(self.n_actions, fc_dims)
        self.optimizer = optim.Adam(self.parameters(), lr=beta)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state, action):
        x = cnn_base(state)
        q1_action_value = self.fc1(T.cat([x, action], dim=1))
        q1_action_value = F.relu(q1_action_value)
        q1 = self.q1(q1_action_value)

        return q1

    def save_checkpoint_check(self, path, id):
        checkpoint = os.path.join(path, self.name+'_td3_'+str(id))
        T.save(self.state_dict(), checkpoint)

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))

class ActorNetwork(nn.Module):
    def __init__(self, name,  input_dims, n_actions, 
            alpha = 0.001, fc_dims = 256, chkpt_dir='subory/'):
        super(ActorNetwork, self).__init__()

        self.n_actions = n_actions
        self.name = str(name)
        self.checkpoint_file = os.path.join(chkpt_dir, name+'_td3')

        self.fc = nn.Linear(576, fc_dims)
        self.mu = nn.Linear(fc_dims, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')

        self.to(self.device)

    def forward(self, state):
        x = cnn_base(state)
        prob = self.fc(x)
        prob = F.relu(prob)
        prob = T.tanh(self.mu(prob)) 
        return prob

    def save_checkpoint_check(self, path, id):
        checkpoint = os.path.join(path, self.name+'_td3_'+str(id))
        T.save(self.state_dict(), checkpoint)

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self, siete):
        file = self.checkpoint_file + '_' + str(siete)
        self.load_state_dict(T.load(file))