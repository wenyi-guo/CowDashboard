from flask import Flask
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import pandas as pd
import json
from datetime import datetime

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


app = Flask(__name__)


@app.route("/weather")
def weather():
    #query = """SELECT c.datesql, c.Animal_ID, c.Group_ID, c.AnimalStatus, c.Gynecology_Status, c["Activity(steps/hr)"], c["Weight(gr)"], c["Yield(gr)"] FROM c WHERE c.Animal_ID = 1"""
    query = """SELECT c.Date, c.highest_temp, c.lowest_temp, c.avg_temp, c.highest_thi, c.lowest_thi, c.avg_thi, c.num_records_on_day FROM c"""
    items = list(weather_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    print(type(items[0]['Date']))
    return {"weather": items}


@app.route("/milk")
def milk():
    #query = """SELECT c.datesql, c.Animal_ID, c.Group_ID, c.AnimalStatus, c.Gynecology_Status, c["Activity(steps/hr)"], c["Weight(gr)"], c["Yield(gr)"] FROM c WHERE c.Animal_ID = 1"""
    query = """SELECT c.datesql, c.Lactation_Num, c["Yield(gr)"], c.Cow_Num FROM c"""
    items = list(milk_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    print(type(items[0]['datesql']))
    return {"milk": items}

@app.route("/")
def milk_sum():
    query_milk = """SELECT c.Date, c.Lactation_Num, c["Yield(gr)"], c.Cow_Num FROM c"""
    items_milk = list(milk_container.query_items(
        query=query_milk,
        enable_cross_partition_query=True
    ))
    milk_df = pd.read_json(json.dumps(items_milk),orient='records')

    query_weather = """SELECT c.Date, c.highest_temp, c.lowest_temp, c.avg_temp, c.highest_thi, c.lowest_thi, c.avg_thi, c.num_records_on_day FROM c"""
    items_weather = list(weather_container.query_items(
        query=query_weather,
        enable_cross_partition_query=True
    ))
    weather_df = pd.read_json(json.dumps(items_weather),orient='records')

    aggregation_functions = {'Lactation_Num': 'first', 'Yield(gr)': 'sum', 'Cow_Num': 'sum'}
    milk_df = milk_df.groupby(milk_df['Date']).aggregate(aggregation_functions)
    df = pd.merge(milk_df, weather_df, on="Date")
    df = df.drop(['Lactation_Num'], axis=1)
    # print(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    result = df.to_json(orient="records")
    parsed = json.loads(result)
    return {"milk":items_milk, "weather": items_weather, "sum":parsed}

if __name__ == "__main__":
    app.run(debug=True)
