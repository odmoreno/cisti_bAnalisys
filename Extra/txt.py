'''
Get abstract and pdf files from csvs
'''
from common_functions import *

years = ['2023', '2022', '2021', '2020', '2019', '2018', '2017',
         '2016', '2015', '2014', '2013', '2012', '2011', '2010']


def loop_years_list():
    mainpath = 'Data/years/'

    for element in years:
        filename = '../'+mainpath + element + '.csv'


if __name__ == '__main__':
  pass
