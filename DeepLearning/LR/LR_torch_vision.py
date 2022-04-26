import numpy as np
import torch
import torch.nn as nn
from torch.utils import data

def synthetic_data(w, b, num_examples): # 生成训练数据
    X = torch.normal(0, 1, (num_examples,len(w)))
    y = torch.matmul(X, w)+b
    y += torch.normal(0, 0.02, y.shape)
    return X , y.reshape((-1,1))


def load_array(data_arrays, batch_size, is_train = True):
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, batch_size, shuffle=is_train)


true_w = torch.tensor([2,-3.4])
true_b = torch.tensor(4.2)
features, labels = synthetic_data(true_w, true_b, 1000)

batch_size = 10
data_iter = load_array((features, labels), batch_size)

# 优化的模型
net = nn.Sequential(nn.Linear(2,1))
net[0].weight.data.normal_(0, 0.01)
net[0].bias.data.fill_(0)

#定义loss和优化函数
MSE = nn.MSELoss()
opt = torch.optim.SGD(net.parameters(),lr = 0.03)

num_epoch = 100
for i in range(num_epoch):
    for X,y in data_iter:
        opt.zero_grad()
        loss = MSE(net(X), y)
        loss.backward()
        opt.step()
    l = MSE(net(features), labels)
    print(f'epoch {i + 1}, loss {l:f}')



