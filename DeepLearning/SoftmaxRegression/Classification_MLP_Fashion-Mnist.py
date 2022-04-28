from itertools import accumulate
import tarfile
import torch
import torch.nn as nn
import torchvision
from torch.utils import data
from torchvision import transforms
import time


class MLP(nn.Module):
    def __init__(self, dim_in, dim_hidden, dim_out):
        super(MLP, self).__init__()
        self.layer_input = nn.Linear(dim_in, dim_hidden)
        self.layer_hidden_1 = nn.Linear(dim_hidden, dim_hidden)
        self.layer_hidden_2 = nn.Linear(dim_hidden, dim_out)
        self.dim_out = dim_out
        self.relu = nn.ReLU()


    def forward(self, x):
        # [256,1,28,28] -> [256,1*28*28]
        # 这个不知道能不能在Sequential里面进行实现
        # 在Sequential中可以用nn.Flatten进行实现
        x = x.view(-1, x.shape[1]*x.shape[2]*x.shape[3])
        x = self.layer_input(x)
        x = self.relu(x)
        x = self.layer_hidden_1(x)
        x = self.relu(x)
        x = self.layer_hidden_2(x)
        return x


def load_data_fashion_mnist(batch_size, resize = None, num_workers = 8):
    trans = [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    if resize :
        trans.insert(0, transforms.Resize(resize))
    trans = transforms.Compose(trans)
    mnist_train = torchvision.datasets.FashionMNIST(root='../data',train = True , transform = trans, download = True)
    mnist_test = torchvision.datasets.FashionMNIST(root='../data',train = False , transform = trans, download = True)

    return data.DataLoader(mnist_train, batch_size, shuffle=True, num_workers=num_workers),data.DataLoader(mnist_test, batch_size, shuffle=False, num_workers=num_workers)


def accuracy(y_hat,y):
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    cmp  = y_hat.type(y.dtype) == y
    return float(cmp.type(y.dtype).sum())


def evaluate_accuracy(net,data_iter):
    if isinstance(net,torch.nn.Module):
        net.eval()
    metric = [0,0]
    for X,y in data_iter:
        metric[0] += accuracy(net(X),y)
        metric[1] += y.numel()
    return metric[0]/metric[1]


num_epochs = 100
batch_size = 256
train_data, test_data = load_data_fashion_mnist(256)

num_inputs = 28*28
num_hidden_neuron = 200
num_outputs = 10

def init_weight(net):
    if type(net) == nn.Linear:
        nn.init.normal_(net.weight,std = 0.05)

net = MLP(num_inputs,num_hidden_neuron,num_outputs)
net.apply(init_weight)
loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(net.parameters(),lr = 0.1)




for epoch in range(num_epochs):
    timer = time.time()
    for X,y in train_data:
        net.train()
        optimizer.zero_grad()
        loss = loss_func(net(X),y)
        loss.backward()
        optimizer.step()
    print(f'test accuracy {evaluate_accuracy(net,test_data)}')
    print(f'epoch {epoch} using {time.time()-timer:.2f} sec')
     