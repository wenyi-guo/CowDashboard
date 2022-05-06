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


@app.route("/sum")
def milk_sum():
    query_milk = """SELECT c.Date, c.Lactation_Num, c["Yield(gr)"], c.Cow_Num FROM c"""
    items_milk = list(milk_container.query_items(
        query=query_milk,
        enable_cross_partition_query=True
    ))
    milk_df = pd.read_json(json.dumps(items_milk), orient='records')
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

    return {"milk": parsed_milk, "weather": parsed_weather, "sum": parsed_sum}


if __name__ == "__main__":
    app.run(debug=True)
