import numpy as np
import torch
from torch.utils.data import Dataset

class ClimateDataset(Dataset):
    def __init__(self, npy_path, seq_len=6):
        self.data = np.load(npy_path)  # (T, H, W)
        self.seq_len = seq_len

    def __len__(self):
        return len(self.data) - self.seq_len

    def __getitem__(self, idx):
        x = self.data[idx:idx + self.seq_len]
        y = self.data[idx + self.seq_len]
        x = torch.tensor(x, dtype=torch.float32).unsqueeze(1)  # (seq_len, 1, H, W)
        y = torch.tensor(y, dtype=torch.float32).unsqueeze(0)  # (1, H, W)
        return x, y
    
