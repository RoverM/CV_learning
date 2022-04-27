from asyncio import FastChildWatcher
from pickletools import optimize
import torch
import torch.nn as nn
import torchvision
from torch.utils import data
from torchvision import transforms

trans = transforms.ToTensor()
mnist_train = torchvision.datasets.FashionMNIST(root='../data',train = True , transform = trans, download = True)
mnist_test = torchvision.datasets.FashionMNIST(root='../data',train = False , transform = trans, download = True)

net = nn.Sequential(#To be the same
        nn.Linear(24*24,18*18),
        nn.Linear(18*18,12*12),
        nn.Linear(12*12,6*6),
        nn.Linear(6*6, 12*12),
        nn.Linear(12*12,18*18),
        nn.Linear(18*18,24*24)    
    )

optimizer = torch.optim.Adam()

print(len(mnist_test))
print(len(mnist_train))