#!/usr/bin/env python3

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets as dts
from torchvision import transforms

print("1")
mnist_train = dts.MNIST(
    root='./data',
    train=True,
    download=True,
    transform=transforms.ToTensor()
)
mnist_test = dts.MNIST(
    root='./data',
    train=False,
    download=True,
    transform=transforms.ToTensor()
)
print("2")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(mnist_train)
print(mnist_test)


train_dataloader = DataLoader(mnist_train, batch_size=64, shuffle=True)
test_dataloader = DataLoader(mnist_test, batch_size=64, shuffle=True)

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(784, 392),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            nn.Linear(392, 196),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            nn.Linear(196, 196),
            nn.ReLU(),
            nn.Linear(196, 10),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)

    for batch, (X, y) in enumerate(dataloader):
        predictions = model(X)
        loss = loss_fn(predictions, y)
        optim.zero_grad()
        loss.backward()
        optim.step()


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size
    print(f'Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n')

model = Model().to(device)
print(model)

loss_fn = nn.CrossEntropyLoss()
lr = 1e-4
#optim = torch.optim.SGD(model.parameters(), lr=lr)
optim = torch.optim.Adam(model.parameters(), lr=lr)

epoch = 100
for t in range(epoch):
    print(f'Epoch {t+1}')
    train_loop(train_dataloader, model, loss_fn, optim)
    if t % 10 == 0:
        test_loop(test_dataloader, model, loss_fn)
