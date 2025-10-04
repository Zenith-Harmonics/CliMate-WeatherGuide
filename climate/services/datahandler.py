import earthaccess
import xarray
import pathlib
import numpy
from sklearn.linear_model import LinearRegression


class Data:
    def __init__(self):
        self.auth = earthaccess.login(strategy="environment")
        self.datasets_path = "merra2datasets"

    def search_data(self, date="01-01"):
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

    def download_data(self, results):
        datasets_paths = []
        for result in results:
            path = earthaccess.download(result, self.datasets_path)
            path_str = str(pathlib.Path(path[0]))
            datasets_paths.append(path_str)
        return datasets_paths

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

