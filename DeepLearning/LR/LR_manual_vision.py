import random
import torch
random.seed(1)


def synthetic_data(w, b, num_examples): # 生成训练数据
    X = torch.normal(0, 1, (num_examples,len(w)))
    y = torch.matmul(X, w)+b
    y += torch.normal(0, 0.02, y.shape)
    return X , y.reshape((-1,1))


def linreg(X,w,b):
    return torch.matmul(X,w)+b


def MSE(y_hat,y):
    return (y_hat-y.reshape(y_hat.shape))**2 / 2


def sgd(params, lr, batch_size):
    with torch.no_grad():
        for param in params:
            param -= lr * param.grad / batch_size
            param.grad.zero_()


def synthetic_data(w,b,num_examples):
    X = torch.normal(0, 1, (num_examples,len(w)))
    y = torch.matmul(X, w)+b
    y += torch.normal(0, 0.01, y.shape)
    return X , y.reshape((-1,1))


def data_iter(batch_size, features, labels):
    num_examples = len(features)
    ind = list(range(num_examples))
    random.shuffle(ind)
    for i in range(0,num_examples,batch_size):
        batch_ind = torch.tensor(ind[i : min(i + batch_size,num_examples)])
        yield features[batch_ind],labels[batch_ind]#yield 太牛了

#生成数据集
true_w = torch.tensor([2,-3.4])
true_b = 4.2
features, labels =synthetic_data(true_w, true_b, 1000)

#需要优化的参数
w = torch.normal(0, 0.01, size=(2,1), requires_grad=True)
b = torch.zeros(1,requires_grad=True)

batch_size = 10

learning_rate = 0.01
num_epochs = 100

# 训练过程
for epoch in range(num_epochs):
    for X,y in data_iter(batch_size,features,labels):
        loss = MSE(linreg(X,w,b),y)
        loss.sum().backward()
        sgd([w,b], 0.01, batch_size)
        with torch.no_grad():
            train_l = MSE(linreg(features,w,b),labels)
            print(f'epoch {epoch + 1}, loss {float(train_l.mean()):f}')

# 比较真实值和学到的参数值
print(f'w的估计误差：{true_w - w.reshape(true_w.shape)}')
print(f'b的估计误差：{true_b - b}')