import torch
import torch.nn as nn
import torch.optim as optim

def create_model():
    # Define the neural network architecture
    model = nn.Sequential(
            nn.Linear(784, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
            )
    return model

def train_model(model, train_data, test_data, bs, l, e):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device) # Ensure the model is on the same device as the data
    # Define the loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=l)

    train_loader = torch.utils.data.DataLoader(train_data, batch_size=bs, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=bs, shuffle=False)

    # Train the model
    for epoch in range(1, e+1):
        train_loss = 0
        train_acc = 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            train_acc += (predicted == labels).sum().item()
        train_loss /= len(train_loader)
        train_acc /= len(train_data)

        # Evaluate the model on the test dataset
        test_loss = 0
        test_acc = 0
        model.eval()
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                test_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                test_acc += (predicted == labels).sum().item()
            test_loss /= len(test_loader)
            test_acc /= len(test_data)

        print(f"Epoch {epoch}/{e} loss: {train_loss:.5f} acc: {train_acc:.5f} val_loss: {test_loss:.5f} val_acc: {test_acc:.5f}")
    return test_acc


# Utility Function to Evaluate the Model
def predict(model, test_loader):
    model.eval()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            return (predicted == labels).sum().item() / len(test_loader)


def generate_data():
    # Generating random data
    train_data = torch.randn((60000, 784))
    train_labels = torch.randint(0, 10, (60000,))
    train_tensor_dataset = torch.utils.data.TensorDataset(train_data, train_labels)

    test_data = torch.randn((10000, 784))
    test_labels = torch.randint(0, 10, (10000,))
    test_tensor_dataset = torch.utils.data.TensorDataset(test_data, test_labels)

    return train_tensor_dataset, test_tensor_dataset


# Define Hyperparameters
bs = 128
l = 0.0001
e = 20

# Generate Data
train_data, test_data = generate_data()

# Create a model instance
model = create_model()

# Train the model
accuracy = train_model(model, train_data, test_data, bs, l, e)

# Evaluate the Model and print the Accuracy
test_loader = torch.utils.data.DataLoader(test_data, batch_size=bs, shuffle=False, num_workers=2)
acc = predict(model, test_loader)
print(f"Accuracy is: {accuracy:.5f} , Evaluated Accuracy is: {acc:.5f}")

# New random function call
new_bs = 256
new_l = 0.001
new_e = 5
new_accuracy = train_model(model, train_data, test_data, new_bs, new_l, new_e)
print(round(new_accuracy, 5))
