import unittest
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# CSV files from the Space Track Satellite Situation Report
# https://www.space-track.org/#ssr


def decayed(filename="~/Downloads/decayed.csv"):
    df = pd.read_csv(filename, parse_dates=['LAUNCH', 'DECAY'])
    df['LAUNCHYEAR'] = pd.DatetimeIndex(df['LAUNCH']).year
    df['DECAYYEAR'] = pd.DatetimeIndex(df['DECAY']).year
    df['DAYSONORBIT'] = df['DECAY'] - df['LAUNCH']
    df['TYPE'] = 'payload'
    df.loc[df['OBJECT_NAME'].str.contains(' DEB'), 'TYPE'] = 'debris'
    df.loc[df['OBJECT_NAME'].str.contains(' R/B'), 'TYPE'] = 'rocket body'
    # df2 = df.groupby(['LAUNCHYEAR','TYPE'], level=1).size()
    df2 = (df.groupby(['LAUNCHYEAR', 'TYPE'])
           .size()
           .unstack(level=-1)
           .reset_index()
           )
    # df2.set_index('LAUNCHYEAR', inplace=True)
    df2.plot.bar(stacked=True, figsize=(16, 9))
    print(df2)
    plt.figure(figsize=(1, 1))
    plt.title("Objects Decayed from LEO")
    plt.savefig('decayed.png')

def inorbit(filename="~/Downloads/inorbit.csv"):
    df = pd.read_csv(filename, parse_dates=['LAUNCH'])
    df['LAUNCHYEAR'] = pd.DatetimeIndex(df['LAUNCH']).year
    df['TYPE'] = 'payload'
    df.loc[df['OBJECT_NAME'].str.contains('STARLINK'), 'TYPE'] = 'constellation'
    df.loc[df['OBJECT_NAME'].str.contains('ONEWEB'), 'TYPE'] = 'constellation'
    df.loc[df['OBJECT_NAME'].str.contains('FLOCK-'), 'TYPE'] = 'constellation'
    df.loc[df['OBJECT_NAME'].str.contains('IRIDIUM'), 'TYPE'] = 'constellation'
    df.loc[df['OBJECT_NAME'].str.contains(' DEB'), 'TYPE'] = 'debris'
    df.loc[df['OBJECT_NAME'].str.contains(' R/B'), 'TYPE'] = 'rocket body'
    df2 = (df.groupby(['LAUNCH', 'TYPE']).size().unstack(level=1).reset_index())
    df2.fillna(0, inplace=True)
    df2['debris'] = df2.debris.cumsum()
    df2['payload'] = df2.payload.cumsum()
    df2['constellation'] = df2.constellation.cumsum()
    df2['rocket body'] = df2['rocket body'].cumsum()
    df2.set_index(['LAUNCH'], inplace=True)
    print(df2.columns)
    my_color = ["#15B01A",'#90EE90','#C0C0C0', '#FF6347' ]

    df2 = df2[['payload', 'constellation', 'rocket body', 'debris']]
    print(df2)
    ax = df2.plot.area(stacked=True, figsize=(16, 9), color=my_color)

    plt.title("Objects in LEO")
    plt.savefig('inorbit.png')


class MyTestCase(unittest.TestCase):
    def test_decayed(self):
        decayed()

    def test_inorbit(self):
        inorbit()


if __name__ == '__main__':
    unittest.main()
