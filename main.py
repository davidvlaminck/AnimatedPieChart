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

    timeseries = {}
    dates = set()
    for record in data:
        date = record[0]
        dates.add(date)
        cat = record[2]

        amount = record[1]
        if date not in timeseries:
            timeseries[date] = {}
        if cat not in timeseries[date]:
            timeseries[date][cat] = 0
        timeseries[date][cat] += int(amount)

    summed_dict = {}
    sum_timeseries = {}
    for date in dates:
        current_d = timeseries[date]
        for cat, amount in current_d.items():
            if cat not in summed_dict:
                summed_dict[cat] = 0
            summed_dict[cat] += amount
        sum_timeseries[date] = summed_dict

    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'limegreen',
              'red', 'navy', 'blue', 'magenta', 'crimson']
    explode = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, .01)
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    fig, ax = plt.subplots()


    def update(num):
        ax.clear()
        ax.axis('equal')
        str_num = str(num)
        for x in range(10):
            nums[x] += str_num.count(str(x))
        ax.pie(nums, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=140)
        ax.set_title(str_num)


    ani = FuncAnimation(fig, update, frames=range(100), repeat=False)
    plt.show()
