import pandas as pd
from datetime import datetime
import json
import time

weather = pd.read_csv('weatherData.csv')
weather = weather[1202:]

print(len(weather))
print(weather[:5])
weather = weather.drop(weather[(weather['AvgBGTemp__P4'].isnull()) & (
    weather['THI_P4'].isnull())].index)
weather = weather.reset_index()
print(len(weather))
print(weather[:5])

newWeather = pd.DataFrame(columns=[
                          'Date', 'highest_temp', 'lowest_temp', 'avg_temp', 'highest_thi', 'lowest_thi', 'avg_thi', 'num_records_on_day'])
first_row = weather.iloc[0]
new_first_row = {}
new_first_row['Date'] = int(time.mktime(datetime.strptime(
    first_row['Date'], '%m/%d/%y %H:%M').date().timetuple()))
new_first_row['highest_temp'] = first_row['AvgBGTemp__P4']
new_first_row['lowest_temp'] = first_row['AvgBGTemp__P4']
new_first_row['avg_temp'] = first_row['AvgBGTemp__P4']
new_first_row['highest_thi'] = first_row['THI_P4']
new_first_row['lowest_thi'] = first_row['THI_P4']
new_first_row['avg_thi'] = first_row['THI_P4']
new_first_row['num_records_on_day'] = 1


newWeather.loc[0] = new_first_row

for i, row in weather.iterrows():
    # print("here", i)
    if i != 0:
        last_i = len(newWeather)-1
        last_row = (newWeather.loc[last_i]).copy()
        row['Date'] = int(time.mktime(datetime.strptime(
            row['Date'], '%m/%d/%y %H:%M').date().timetuple()))
        if row['Date'] == last_row['Date']:
            if row['AvgBGTemp__P4'] > last_row['highest_temp']:
                last_row['highest_temp'] = row['AvgBGTemp__P4']
            if row['AvgBGTemp__P4'] < last_row['lowest_temp']:
                last_row['lowest_temp'] = row['AvgBGTemp__P4']
            if row['THI_P4'] > last_row['highest_thi']:
                last_row['highest_thi'] = row['THI_P4']
            if row['THI_P4'] < last_row['lowest_thi']:
                last_row['lowest_thi'] = row['THI_P4']
            last_row['avg_temp'] = (last_row['avg_temp'] *
                                    last_row['num_records_on_day'] + row['AvgBGTemp__P4']) / (last_row['num_records_on_day'] + 1)
            last_row['avg_thi'] = (last_row['avg_thi'] *
                                   last_row['num_records_on_day'] + row['THI_P4']) / (last_row['num_records_on_day'] + 1)
            last_row['num_records_on_day'] += 1
            newWeather.loc[len(newWeather)-1] = last_row
        else:
            new_row = {}
            new_row['Date'] = row['Date']
            new_row['highest_temp'] = row['AvgBGTemp__P4']
            new_row['lowest_temp'] = row['AvgBGTemp__P4']
            new_row['avg_temp'] = row['AvgBGTemp__P4']
            new_row['highest_thi'] = row['THI_P4']
            new_row['lowest_thi'] = row['THI_P4']
            new_row['avg_thi'] = row['THI_P4']
            new_row['num_records_on_day'] = 1
            newWeather.loc[len(newWeather)] = new_row

print(newWeather[:10])

newWeather.to_csv('weather.csv', index=False)
newWeather.to_json("weather.json", orient='records')
