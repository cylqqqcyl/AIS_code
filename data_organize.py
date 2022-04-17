import pandas as pd
import os
import numpy as np

path = u'dataset'

os.chdir(path)
count =0
# prefile = os.listdir()[0]
# predate = prefile.strip('.txt')[:9]
colnames = ['date','time', 'ID', 'prelong', 'prelat', 'long', 'lat',  'speed', 'angle', 'NA']
colnames2 = ['17', '18','19','20','21','22','23','24','25']
# pre_data = pd.read_csv(prefile, names=colnames, sep='\s+')


if __name__ == '__main__':
    for file in os.listdir():
        zerodata = np.zeros(shape=(24, 9))
        by_hour = pd.DataFrame(zerodata,columns=colnames2)
        if file.endswith('.csv'):
            data = pd.read_csv(file)
            dates = []
            date17 = data[data['date'].isin(['2016-10-17'])]
            dates.append(date17)
            date18 = data[data['date'].isin(['2016-10-18'])]
            dates.append(date18)
            date19 = data[data['date'].isin(['2016-10-19'])]
            dates.append(date19)
            date20 = data[data['date'].isin(['2016-10-20'])]
            dates.append(date20)
            date21 = data[data['date'].isin(['2016-10-21'])]
            dates.append(date21)
            date22 = data[data['date'].isin(['2016-10-22'])]
            dates.append(date22)
            date23 = data[data['date'].isin(['2016-10-23'])]
            dates.append(date23)
            date24 = data[data['date'].isin(['2016-10-24'])]
            dates.append(date24)
            date25 = data[data['date'].isin(['2016-10-25'])]
            dates.append(date25)
            for date in dates:
                date.sort_values('time', inplace=True)
                date['time'] = pd.to_datetime(date['time'], format='%Y-%m-%d %H:%M:%S')
                for row in date.iterrows():
                    hour = row[1]['time'].hour
                    by_hour.iloc[hour][date.iloc[0]['date'][-2:]] += 1
                print(f"{date.iloc[0]['date']}:{date.shape[0]}")
            print(by_hour)
            by_hour.to_csv("hour_table.csv")


