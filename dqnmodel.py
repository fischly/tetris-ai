import numpy as np
import pandas as pd
import seaborn as sns
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class DQNModel():
    def __init__(self, update_frequency, load_from_file=None):
        self.update_frequency = update_frequency
        self.update_counter = 0
        
        self.model = self.create_model()
        self.target_model = self.create_model()
        
        if load_from_file is not None:
            self.model.load_state_dict(torch.load(load_from_file))
        
        # make the parameters of both models the same to start with
        self.update_target()
        
    def create_model(self):
        # layer initialisation
        def init_linear_layer(m, method):
            torch.nn.init.xavier_normal_(m.weight, nn.init.calculate_gain(method))
            torch.nn.init.constant_(m.bias, 0)
            return m
        
        model = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            
            nn.Flatten(),
            
            init_linear_layer(nn.Linear(1*6*64, 256), 'relu'),
            nn.ReLU(),
            init_linear_layer(nn.Linear(256, 128), 'relu'),
            nn.ReLU(),
            init_linear_layer(nn.Linear(128, 1), 'linear')
        )
        
        # model = nn.Sequential(
        #     nn.Flatten(),
        #     init_linear_layer(nn.Linear(20*10, 128), 'relu'),
        #     nn.ReLU(),
        #     init_linear_layer(nn.Linear(128, 64), 'relu'),
        #     nn.ReLU(),
        #     init_linear_layer(nn.Linear(64, 32), 'relu'),
        #     nn.ReLU(),
        #     init_linear_layer(nn.Linear(32, 1), 'linear')
        # )
        
        return model
    
    def update_target(self):
        for param, target_param in zip(self.model.parameters(), self.target_model.parameters()):
            target_param.data.copy_(param)
    
    def step(self):
        self.update_counter += 1
        
        if self.update_counter >= self.update_frequency:
            print(f'[DQNModel] updating target network')
            self.update_counter -= self.update_frequency
            
            self.update_target()
    
    
    def to(self, device):
        self.model.to(device)
        self.target_model.to(device)
