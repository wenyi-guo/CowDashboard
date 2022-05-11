import pandas as pd
import json

import datetime
import time
import re

from sqlalchemy import null


def time_str_to_datetime(time_str):
    date = re.split('-| ', str(time_str))
    date_time = datetime.datetime(
        int(f"{date[0]}"), int(date[1]), int(date[2]), 0, 0)
    return pd.to_datetime(time.mktime(date_time.timetuple()), unit='s')


def process_rumination(raw_rumination_data):
    raw_df = pd.read_json(json.dumps(raw_rumination_data), orient='records')
    if not raw_df.empty:
        rum_df = raw_df[["observation_time",
                         "total_rumination", "total_eating"]].copy()
        rum_df['observation_time'] = rum_df['observation_time'].apply(
            time_str_to_datetime)
        rum_df.rename(columns={'observation_time': 'Date'}, inplace=True)
        # print(rum_df)
        rum_df['rumination_count'] = rum_df['total_rumination'].apply(
            lambda x: int(x >= 1))
        rum_df['eating_count'] = rum_df['total_eating'].apply(
            lambda x: int(x >= 1))
        rum_df_sum = rum_df.groupby(['Date'], as_index=False, sort=True).sum()
        rum_df_sum.groupby(['Date'], as_index=False).agg(
            {'rumination_count': 'sum', 'eating_count': 'sum', 'total_rumination': 'sum', 'total_eating': 'sum'})
        return rum_df_sum
    return raw_df
