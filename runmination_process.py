import pandas as pd
import json

import datetime
import time
import re

def time_str_to_unix(time_str):
    
    date = re.split('-| ',str(time_str))
    date_time = datetime.datetime(int(f"{date[0]}"), int(date[1]), int(date[2]), 0, 0)
    # displaying unix timestamp after conversion
    # print("unix_timestamp => ",
    #   (time.mktime(date_time.timetuple())))
    return int(time.mktime(date_time.timetuple()))

message = [{
    "id": 456,
    "cow_id": 2020,
    "total_eating": 1,
    "total_rumination": 1,
    "observation_time": "2019-01-01 01:00:12.575757+00",
    "hour_complete": 2,
    "local_id": 25,

},{
    "id": 457,
    "cow_id": 2020,
    "total_eating": 2,
    "total_rumination": 2,
    "observation_time": "2019-01-01 01:00:12.575757+00",
    "hour_complete": 2,
    "local_id": 25,

}, 
{
    "id": 458,
    "cow_id": 2020,
    "total_eating": 3,
    "total_rumination": 3,
    "observation_time": "2019-01-02 01:00:12.575757+00",
    "hour_complete": 3,
    "local_id": 25,

}]

def process_rumination(raw_rumination_data):

    raw_df = pd.read_json(json.dumps(raw_rumination_data), orient='records')
    rum_df = raw_df[["observation_time","total_rumination", "total_eating"]].copy()
    rum_df['observation_time'] = rum_df['observation_time'].apply(time_str_to_unix)
    rum_df.rename(columns={'observation_time':'Date'}, inplace=True)
    # print(rum_df) 
    rum_df['rumination_count'] = rum_df['total_rumination'].apply(lambda x: int(x>=1) )
    rum_df['eating_count'] = rum_df['total_eating'].apply(lambda x: int(x>=1))
    rum_df_sum = rum_df.groupby(['Date'], as_index=False, sort = True).sum()
    rum_df_sum['id'] = rum_df_sum['Date'].apply(lambda x: str(x))

    print(rum_df_sum)

    return rum_df_sum


process_rumination(message)