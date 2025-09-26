import torch
import torch.nn as nn
import torch.nn.functional as F


# class DQN(nn.Module):
#     def __init__(self, n_observations, n_actions):
#         super(DQN, self).__init__()
#         self.layer1 = nn.Linear(n_observations, 128)
#         self.layer2 = nn.Linear(128, 128)
#         self.layer3 = nn.Linear(128, n_actions)


#     def forward(self, x):
#         x = x.float()
#         x = F.relu(self.layer1(x))
#         x = F.relu(self.layer2(x))
#         return self.layer3(x)


import torch
import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):
    def __init__(self, n_actions):
        super(DQN, self).__init__()  # input: (batch, 1, 10, 10)
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1)  # -> (batch, 32, 8, 8)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1)  # -> (batch, 64, 6, 6)
        self.fc1 = nn.Linear(64 * 6 * 6, 128)
        self.fc2 = nn.Linear(128, n_actions)

    def forward(self, x):
        x = x.float()
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # flatten
        x = F.relu(self.fc1(x))
        return self.fc2(x)
