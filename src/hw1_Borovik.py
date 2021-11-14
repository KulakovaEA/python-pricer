class Interpolator:

    def interpolate(x_list: list, y_list: list, z: float):
        if x_list != sorted(x_list):
            raise ValueError('x_list must be sorted ASC')
        for index, element in enumerate(x_list):
            if z <= element:
                delta = (z - x_list[index - 1]) / (x_list[index] - x_list[index - 1])
                answer = y_list[index - 1] + (y_list[index] - y_list[index - 1]) * delta
                break
        return answer
      

import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings("ignore")

dates = pd.DataFrame([
    {"dates": '12-04-22'}, 
    {"dates": '03-05-22'},
    {"dates": '19-07-22'},
    {"dates": '17-11-22'},
    {"dates": '21-12-22'},
    {"dates": '04-02-23'},
    {"dates": '24-03-23'},
    {"dates": '16-05-23'},
    {"dates": '18-07-23'},
    {"dates": '05-08-22'},
])

def dummy_func(dates):
    return([0.99]*len(dates))
  
swaps = pd.DataFrame([
    {"date": '11-03-22', "swap points":627}, 
    {"date": '12-05-22', "swap points": 1253}, 
    {"date": '21-09-22', "swap points": 1300}, 
    {"date": '29-10-22', "swap points": 2456}, 
    {"date": '01-12-22', "swap points": 1356}, 
    {"date": '11-01-23', "swap points": 3456}, 
    {"date": '15-03-23', "swap points": 5216}, 
    {"date": '16-04-23', "swap points": 6708}, 
    {"date": '10-06-23', "swap points": 8071}, 
    {"date": '26-08-23', "swap points": 9023}])
for a in range(len(swaps)):
    swaps['date'][a] = datetime.datetime.strptime(swaps['date'][a], '%d-%m-%y')
swaps['timestamp'] = swaps['date'].apply(lambda x: x.timestamp())

def interpolated_swap_point(date):
  date1 = datetime.datetime.strptime(date, '%d-%m-%y')
  return Interpolator.interpolate(list(swaps['timestamp']), list(swaps['swap points']), date1.timestamp())

dates['swap_points'] = dates['dates'].apply(interpolated_swap_point)

def years_between(d2, d1 = '5-11-21'): #вспомогательная функция, считает время, прошедшее с сегодняшнего дня
    d1 = datetime.datetime.strptime(d1, "%d-%m-%y")
    d2 = datetime.datetime.strptime(d2, "%d-%m-%y")
    return abs((d2 - d1).days)/365
  
dates['df_usd'] = dummy_func(dates['dates'])
dates['rate_usd'] = dates['df_usd'].apply(lambda x: -np.log(x)/years_between(dates['dates'][dates['df_usd'] == x].values[0]))

def get_rate_rub(points, r_usd, spot = 71):
    return((points/(100*spot)+1)*(1+r_usd) - 1)

dates['rate_rub'] = dates.apply(lambda x: get_rate_rub(x.swap_points, x.rate_usd), axis=1)

dates['df_rub'] = dates['rate_rub'].apply(lambda x: np.exp(-x*years_between(dates['dates'][dates['rate_rub'] == x].values[0])))
