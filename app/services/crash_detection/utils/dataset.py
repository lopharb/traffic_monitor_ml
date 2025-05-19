import os
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms


class TrafficDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.root_dir = root_dir
        self.transform = transform or transforms.ToTensor()

        # Get list of image paths
        self.image_paths = [
            os.path.join(root_dir, img) for img in os.listdir(root_dir)
            if img.endswith(('.png', '.jpg', '.jpeg'))
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image
