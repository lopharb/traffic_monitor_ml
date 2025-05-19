import torch.nn as nn


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, activation='relu'):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(out_channels)
        if activation == 'relu':
            self.activation = nn.ReLU(inplace=True)
        elif activation == 'sigmoid':
            self.activation = nn.Sigmoid()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.activation(x)
        return x


class CrashDetectionAutoencoder(nn.Module):
    def __init__(self):
        super(CrashDetectionAutoencoder, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            ConvBlock(3, 8),    # 3x224x224 → 3x224x224
            ConvBlock(8, 16),  # 3x224x224 → 16x112x112
            ConvBlock(16, 32),  # 16x112x112 → 32x56x56
            ConvBlock(32, 64),  # 32x56x56 → 64x28x28
        )

        # Decoder
        self.decoder = nn.Sequential(
            ConvBlock(64, 32),  # 64x28x28 → 32x56x56
            ConvBlock(32, 16),  # 32x56x56 → 16x112x112
            ConvBlock(16, 8),   # 16x112x112 → 8x224x224
            ConvBlock(8, 3, 'sigmoid')
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
