import copy
import datetime
from collections import OrderedDict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import dataset
from SheetsWrapper import SheetsWrapper

if __name__ == '__main__':
    wrapper = SheetsWrapper(
        service_cred_path=Path("/home/davidlinux/Documents/AWV/resources/driven-wonder-149715-ca8bdf010930.json"),
        readonly_scope=True)
    # data = wrapper.read_data_from_sheet(
    #     spreadsheet_id='1183HYO96A4-0Wih3jpi1DWm9fXSXMZQhpKD3Pd-eJuM',
    #     sheet_name='Data', sheetrange='A2:C1000')

    data = dataset.data

    timeseries = OrderedDict()
    for record in data:
        date = record[0]
        cat = record[2]

        amount = record[1]
        if date not in timeseries:
            timeseries[date] = {}
        if cat not in timeseries[date]:
            timeseries[date][cat] = 0
        timeseries[date][cat] += int(amount)

    summed_dict = {}
    sum_timeseries = {}
    for date in list(timeseries.keys()):
        current_d = timeseries[date]
        for cat, amount in current_d.items():
            if cat not in summed_dict:
                summed_dict[cat] = 0
            summed_dict[cat] += amount
        sum_timeseries[date] = copy.deepcopy(summed_dict)

    labels = list(summed_dict.keys())
    fig, ax = plt.subplots()

    dates = list(timeseries.keys())

    def update(num):
        ax.clear()
        ax.axis('equal')
        dt = dates[num]

        values = []
        for label in labels:
            if label in sum_timeseries[dt]:
                values.append(sum_timeseries[dt][label])
            else:
                values.append(0)

        ax.pie(values, labels=labels, shadow=True, startangle=140)
        ax.set_title(dt)


    ani = FuncAnimation(fig, update, frames=len(dates), repeat=False)
    ani.save('pie_chart_2.gif', writer='imagemagick', fps=2)
    plt.show()
