from flask import Flask
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import pandas as pd
import json
from datetime import datetime
import time
from runmination_process import process_rumination

endpoint = "https://diaryinstance.documents.azure.com:443/"

key = 'y5ZatCRxHYVOmYkBpwfP1nJV9yiR5zzyULXetVwZlG97CRUvQ46hfIXg9e9Nlv84aR0742L1YoIMao11NB8GmA=='
client = CosmosClient(endpoint, key)
database_name = "dairyDB"
database = client.create_database_if_not_exists(id=database_name)

weather_container = database.create_container_if_not_exists(
    id="weather",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
milk_container = database.create_container_if_not_exists(
    id="daily_milk",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
rum_container = database.create_container_if_not_exists(
    id="rumination",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
database_name_temp = "dairyTemp"
database_temp = client.create_database_if_not_exists(id=database_name_temp)
milk_input_container = database_temp.create_container_if_not_exists(
    id="milk_temp",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
rum_input_container = database_temp.create_container_if_not_exists(
    id="rum_temp",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
weather_input_container = database_temp.create_container_if_not_exists(
    id="weather_temp",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)


gram_to_lb = 0.00220462

app = Flask(__name__)


@app.route("/weather")
def weather():
    # query = """SELECT c.datesql, c.Animal_ID, c.Group_ID, c.AnimalStatus, c.Gynecology_Status, c["Activity(steps/hr)"], c["Weight(gr)"], c["Yield(gr)"] FROM c WHERE c.Animal_ID = 1"""
    query = """SELECT c.Date, c.highest_temp, c.lowest_temp, c.avg_temp, c.highest_thi, c.lowest_thi, c.avg_thi FROM c"""
    items = list(weather_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    print(type(items[0]['Date']))
    return {"weather": items}


@app.route("/milk")
def milk():
    # query = """SELECT c.datesql, c.Animal_ID, c.Group_ID, c.AnimalStatus, c.Gynecology_Status, c["Activity(steps/hr)"], c["Weight(gr)"], c["Yield(gr)"] FROM c WHERE c.Animal_ID = 1"""
    query = """SELECT c.Date, c.Lactation_Num, c["Yield(gr)"], c.Cow_Num FROM c"""
    items = list(milk_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    print(type(items[0]['Date']))
    return {"milk": items}

def time_str_to_unix(time_str):
    # print(time_str.timestamp())
    return time_str.timestamp()

def process_milk_input():
    query_milk_input = """SELECT c.Date, c.Lactation_Num, c.Yield FROM c"""
    
    items_milk_input = list(milk_input_container.query_items(
        query=query_milk_input,
        enable_cross_partition_query=True
    ))
    milk_input_data = pd.read_json(json.dumps(items_milk_input), orient='records')

    milk_df_input = pd.DataFrame([], columns = ['Date', 'Lactation_Num','Yield(gr)','Cow_Num'])
    for index, row in milk_input_data.iterrows():
        if row['Yield'] > 0:
            milk_df_input = milk_df_input.append({'Date': row['Date'], 'Lactation_Num':row["Lactation_Num"], 'Yield(gr)': row['Yield'], 'Cow_Num': 1}, ignore_index=True)

    new_df = milk_df_input.groupby(['Date','Lactation_Num'], as_index=False).agg({"Yield(gr)": 'sum', 'Cow_Num':'sum'})
    for index, row in new_df.iterrows():
        new_df['id'] = str(time_str_to_unix(row['Date']))+"_"+str(float(row['Lactation_Num']))
    return new_df


@app.route("/sum")
def milk_sum():
    query_rum = """SELECT c.Date, c.total_rumination, c.total_eating, c.rumination_count, c.eating_count FROM c"""
    items_rum = list(rum_container.query_items(
        query=query_rum,
        enable_cross_partition_query=True
    ))
    rum_df = pd.read_json(json.dumps(items_rum), orient='records')
    query_rum_temp = """SELECT c.observation_time, c.total_eating, c.total_rumination FROM c"""
    items_rum_temp = list(rum_input_container.query_items(
        query=query_rum_temp,
        enable_cross_partition_query=True
    ))
    processed_rum = process_rumination(items_rum_temp)
    rum_df = rum_df.append(processed_rum) if not processed_rum.empty else rum_df

    rum_df['Date'] = rum_df['Date'].dt.strftime('%Y-%m-%d')
    rum_df.rename(columns={'total_rumination': 'Total rumination',
                           'total_eating': 'Total eating'}, inplace=True)
    rum_df['Average rumination'] = rum_df['Total rumination'] / \
        rum_df['rumination_count']
    rum_df['Average eating'] = rum_df['Total eating'] / rum_df['eating_count']
    parsed_rum = json.loads(rum_df.to_json(orient="records"))


    query_milk = """SELECT c.id, c.Date, c.Lactation_Num, c["Yield(gr)"], c.Cow_Num FROM c"""
    items_milk = list(milk_container.query_items(
        query=query_milk,
        enable_cross_partition_query=True
    ))
    milk_df = pd.read_json(json.dumps(items_milk), orient='records')
    milk_input_df = process_milk_input()
    milk_df = milk_df.append(milk_input_df)

    milk_df['Date'] = milk_df['Date'].dt.strftime('%Y-%m-%d')

    milk_df['Yield(gr)'] = milk_df['Yield(gr)'] * gram_to_lb
    milk_df.rename(columns={'Yield(gr)': 'Yield (lb)',
                            'Lactation_Num': 'Lactation number'}, inplace=True)
    milk_df.loc[milk_df['Lactation number'] >= 3, 'Lactation number'] = '3+'

    query_weather = """SELECT c.Date, c.highest_temp, c.lowest_temp, c.avg_temp, c.highest_thi, c.lowest_thi, c.avg_thi FROM c"""
    items_weather = list(weather_container.query_items(
        query=query_weather,
        enable_cross_partition_query=True
    ))
    weather_df = pd.read_json(json.dumps(items_weather), orient='records')
    weather_df['Date'] = weather_df['Date'].dt.strftime('%Y-%m-%d')
    weather_df.rename(columns={'avg_temp': 'Average temperature (°C)', 'avg_thi': 'Average THI', 'highest_temp': 'Highest temperature',
                               'highest_thi': 'Highest THI', 'lowest_temp': 'Lowest temperature', 'lowest_thi': 'Lowest THI'}, inplace=True)

    aggregation_functions = {'Lactation number': 'first',
                             'Yield (lb)': 'sum', 'Cow_Num': 'sum'}
    milk_df_temp = milk_df.groupby(
        milk_df['Date']).aggregate(aggregation_functions)
    df = pd.merge(milk_df_temp, weather_df, on="Date")
    df = df.drop(['Lactation number'], axis=1)
    df = df.drop(['Highest temperature', 'Highest THI',
                  'Lowest temperature', 'Lowest THI'], axis=1)
    df['Average yield (lb)'] = (df['Yield (lb)']/df['Cow_Num'])
    df = df.astype({"Average yield (lb)": int})

    result_sum = df.to_json(orient="records")
    parsed_sum = json.loads(result_sum)

    milk_df['Average yield (lb)'] = (milk_df['Yield (lb)']/milk_df['Cow_Num'])
    milk_df = milk_df.astype({"Average yield (lb)": int})
    milk_df = milk_df.drop(['Cow_Num'], axis=1)
    result_milk = milk_df.to_json(orient="records")
    parsed_milk = json.loads(result_milk)

    result_weather = weather_df.to_json(orient="records")
    parsed_weather = json.loads(result_weather)

    return {"milk": parsed_milk, "weather": parsed_weather, "sum": parsed_sum, "rum": parsed_rum}


if __name__ == "__main__":
    app.run(debug=True)
