import time

import earthaccess
import xarray as xr
import datetime


class Data:
    def __init__(self):
        self.auth = earthaccess.login(strategy="environment")
        self.datasets_path = "merra2datasets"

    def search_data(self, date="01-01"):
        results = []
        for i in range(0, 3):
            result = earthaccess.search_data(
                short_name='M2T1NXSLV',
                temporal=(f"200{i}-{date}", f"200{i}-{date}"),
                count=10
            )

            results.append(result)

        return results

    def download_data(self, results):
        datasets_path = []
        for result in results:
            datasets_path.append(earthaccess.download(result, self.datasets_path))





if __name__ == "__main__":
    data = Data()

    results = data.search_data(date="01-02")
    print(data.download_data(results))

