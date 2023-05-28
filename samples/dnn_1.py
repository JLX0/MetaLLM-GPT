import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import OneCycleLR
import time

# Define the deep neural network
class DNN(nn.Module):

    def __init__(self):
        super(DNN, self).__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(28 * 28, 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        x = self.layers(x)
        return x


def train_deep_neural_network(bs: int = 64, l: float = 0.001, e: int = 10, lr_factor: float = 10, lr_pctg: float = 0.3, wd: float = 0.01, momentum: float = 0.9, max_lr: float = 0.05) -> float:
    # Create the train and test datasets and dataloaders
    train_dataset = datasets.MNIST(
        root="data/", train=True, transform=transforms.ToTensor(), download=True
    )
    test_dataset = datasets.MNIST(
        root="data/", train=False, transform=transforms.ToTensor(), download=True
    )
    train_dataloader = DataLoader(
        dataset=train_dataset, batch_size=bs, shuffle=True, num_workers=4
    )
    test_dataloader = DataLoader(
        dataset=test_dataset, batch_size=bs, shuffle=False, num_workers=4
    )

    # Initialize the neural network and move it to GPU if available
    net = DNN()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.to(device)

    # Define the loss function, optimizer and learning rate scheduler
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=l, momentum=momentum, weight_decay=wd)
    scheduler = OneCycleLR(
        optimizer,
        max_lr=max_lr,
        epochs=e,
        steps_per_epoch=len(train_dataloader),
        pct_start=lr_pctg / 2,
        div_factor=lr_factor,
    )

    # Train and validate the neural network
    for epoch in range(1, e + 1):
        start_time = time.monotonic()
        net.train()
        train_loss = []

        for batch_idx, (data, target) in enumerate(train_dataloader, 1):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = net(data)
            loss = criterion(output, target)
            train_loss.append(loss.item())

            loss.backward()
            optimizer.step()
            scheduler.step()

        train_loss = sum(train_loss) / len(train_loss)

        net.eval()
        correct_count, total_count = 0, 0
        with torch.no_grad():
            for data, target in test_dataloader:
                data, target = data.to(device), target.to(device)
                output = net(data)
                _, predicted = torch.max(output.data, 1)
                total_count += target.size(0)
                correct_count += (predicted == target).sum().item()
        val_acc = 100 * correct_count / total_count

        print(
            f"Epoch {epoch}, Test Accuracy: {val_acc:.2f}%, Train Loss: {train_loss:.4f}, Time: {time.monotonic()-start_time:.2f}s"
        )

    # Print the last accuracy
    print(f"Final Test Accuracy: {val_acc:.2f}%")

    return val_acc


# Example function call to train deep neural network
train_deep_neural_network(bs=128, l=0.0001, e=15, lr_factor=6, max_lr=0.01, lr_pctg=0.2, wd=2e-3, momentum=0.95)
