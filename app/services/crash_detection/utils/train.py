import os
import cv2
import torch
from app.services.crash_detection.model import CrashDetectionAutoencoder
from torch.utils.data import DataLoader
from app.services.crash_detection.utils.dataset import TrafficDataset
from typing import Type
from tqdm import tqdm
from torchvision import transforms


def train(
    epochs: int,
    train_set: TrafficDataset,
    test_set: TrafficDataset,
    model_type: Type[CrashDetectionAutoencoder],
    batch_size: int,
    checkpoint_period: int,
    checkpoint_path: str
):

    TEMPLATE = "Epoch [{:04}/{:04}] | Mean Train Loss: {:.4f} | Mean Test Loss: {:.4f}"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model_type().to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.MSELoss()

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

    for e in range(1, epochs+1):
        test_loss = 0
        train_loss = 0
        for batch in tqdm(train_loader):
            batch = batch.to(device)
            output = model(batch)
            loss = criterion(output, batch)

            optimizer.zero_grad()
            train_loss += loss.item()
            loss.backward()
            optimizer.step()

        for batch in tqdm(test_loader):
            batch = batch.to(device)
            output = model(batch)
            loss = criterion(output, batch)
            test_loss += loss.item()

            # Display the original and prediction on screen
            original = batch[0].detach().cpu().numpy().transpose(1, 2, 0)
            prediction = output[0].detach().cpu().numpy().transpose(1, 2, 0)
            cv2.imshow("Original", original)
            cv2.imshow("Prediction", prediction)
            cv2.waitKey(1)

        print(TEMPLATE.format(e, epochs, train_loss/len(train_loader), test_loss/len(test_loader)))

        if e % checkpoint_period == 0:
            torch.save(model.state_dict(), os.path.join(checkpoint_path, f"checkpoint_{e}.pt"))


if __name__ == "__main__":
    transforms = transforms.Compose([
        transforms.Resize((448, 448)),
        transforms.ToTensor()
    ])

    train_set = TrafficDataset("test_images", transform=transforms)
    test_set = TrafficDataset("test_images", transform=transforms)

    train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=32, shuffle=False)

    train(
        epochs=50,
        train_set=train_set,
        test_set=test_set,
        model_type=CrashDetectionAutoencoder,
        batch_size=32,
        checkpoint_period=2,
        checkpoint_path=""
    )
