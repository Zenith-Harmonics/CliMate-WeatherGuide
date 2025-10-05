from .dataset_wrapper import ClimateDataset
from .datahandler import MERRA2Downloader
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import earthaccess
import xarray as xr
import numpy as np
from services.ml_architecture import ConvLSTMModel

earthaccess.login(strategy="netrc")


# Step 1: Download and preprocess 2000–2019 Europe data
region = {"lat": (30, 60), "lon": (-10, 30)}  # Europe
downloader = MERRA2Downloader()
all_years = []

for year in range(2000, 2020):
    nc_files = downloader.download_year(year)
    monthly = downloader.preprocess_to_monthly(nc_files, region=region)
    all_years.append(monthly)

data = xr.concat(all_years, dim="time")
data_np = data.values  # shape: (T, H, W)
np.save("merra2_europe_t2m.npy", data_np.astype(np.float32))
print("✅ Saved full Europe dataset:", data_np.shape)

# Step 2: Training
def train_model(npy_path, epochs=10, batch_size=4, lr=1e-3):
    dataset = ClimateDataset(npy_path, seq_len=6)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = ConvLSTMModel(input_dim=1, hidden_dim=32, kernel_size=3, output_dim=1)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for X, Y in train_loader:
            optimizer.zero_grad()
            preds = model(X)
            loss = criterion(preds, Y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}: Loss = {total_loss / len(train_loader):.6f}")

    return model

# Actually train
model = train_model("merra2_europe_t2m.npy", epochs=20, batch_size=4)
torch.save(model.state_dict(), "convlstm_weather.pt")
print("✅ Model saved as convlstm_weather.pt")