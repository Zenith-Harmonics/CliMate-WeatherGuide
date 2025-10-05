import earthaccess
import xarray
import pathlib
from pathlib import Path
import numpy
from sklearn.linear_model import LinearRegression
import xarray as xr
import numpy as np


class Data:
    def __init__(self):
        self.auth = earthaccess.login(strategy="token")
        self.datasets_path = Path("merra2datasets")
        self.datasets_path.mkdir(exist_ok=True)

    def search_data(self, date="01-01"):
        results = []
        for year in range(2000, 2020):
            result = earthaccess.search_data(
                short_name="M2T1NXSLV",
                temporal=(f"{year}-{date}", f"{year}-{date}"),
                count=1
            )
            results.append(result)
        return results

    def download_data(self, results):
        downloaded_files = []
        for result in results:
            for granule in result:
                local_path = self.datasets_path / pathlib.Path(granule.data_links()[0]).name
                if not local_path.exists():
                    earthaccess.download(granule, str(self.datasets_path))
                downloaded_files.append(str(local_path))
        return downloaded_files

    def load_data_grid(self, paths, var="T2M", lat_range=None, lon_range=None):
        """Load T2M data for a region or the whole globe"""
        datasets = []
        for path in paths:
            ds = xr.open_dataset(path)
            data = ds[var] - 273.15  # Kelvin → °C

            if lat_range and lon_range:
                data = data.sel(lat=slice(*lat_range), lon=slice(*lon_range))

            # Mean over time dimension if hourly
            if "time" in data.dims:
                data = data.mean(dim="time")

            datasets.append(data)

        # Stack along the "year" axis
        data_array = xr.concat(datasets, dim="year")
        return data_array

    def preprocess_to_numpy(self, data_array, save_path="preprocessed_data.npy"):
        """Convert xarray DataArray to numpy (T, H, W) and save"""
        np_data = data_array.values  # shape: (years, lat, lon)
        np.save(save_path, np_data)
        return np_data

    def search_data_by_date(self, date="01-01"):
        results = []
        for i in range(0, 20):
            result = []
            if i < 10:
                result = earthaccess.search_data(
                short_name='M2T1NXSLV',
                temporal=(f"200{i}-{date}", f"200{i}-{date}"),
                count=10
                )
            else:
                result = earthaccess.search_data(
                    short_name='M2T1NXSLV',
                    temporal=(f"20{i}-{date}", f"20{i}-{date}"),
                    count=10
                )

            results.append(result)
        return results



    def load_data(self, paths, lat = 45.943, lon = 24.96):
        datasets = []
        for path in paths:
            dataset = xarray.open_dataset(path)
            t2m = dataset['T2M'] - 273.15
            t2m_point = t2m.sel(lat=lat, lon=lon, method='nearest')
            datasets.append(t2m_point.values.tolist())
        return datasets

    def calculate_prediction(self, dataset):
        years = numpy.array([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]).reshape(-1, 1)
        yearly_mean = numpy.array([numpy.mean(day) for day in dataset])

        model = LinearRegression()
        model.fit(years, yearly_mean)
        prediction = model.predict(numpy.array([[2025]]))[0]

        return prediction


def do_the_thing(date="01-01", lat=0.0, lon=0.0):
    data = Data()

    results = data.search_data(date)
    datasets_paths = data.download_data(results)
    dataset = data.load_data(datasets_paths, lat, lon)
    print(data.calculate_prediction(dataset))


do_the_thing(date="01-01", lat=45.943, lon=24.96)




class MERRA2Downloader:
    def __init__(self):
        self.auth=earthaccess.login(strategy="netrc")
        self.data_dir = Path("merra2_cache")
        self.data_dir.mkdir(exist_ok=True)

    def download_year(self, year, short_name="M2T1NXSLV"):
        results = earthaccess.search_data(
            short_name=short_name,
            temporal=(f"{year}-01-01", f"{year}-12-31"),
            count=-1
        )
        return earthaccess.download(results, str(self.data_dir))

    def preprocess_to_monthly(self, nc_files, region=None):
        datasets = []
        for f in nc_files:
            ds = xr.open_dataset(f)
            da = ds["T2M"] - 273.15  # Kelvin → °C
            if region:
                da = da.sel(lat=slice(*region["lat"]), lon=slice(*region["lon"]))
            da_monthly = da.resample(time="1M").mean()
            datasets.append(da_monthly)
        merged = xr.concat(datasets, dim="time")
        return merged





