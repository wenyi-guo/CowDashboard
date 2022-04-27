from flask import Flask
from azure.cosmos import exceptions, CosmosClient, PartitionKey

endpoint = "https://diaryinstance.documents.azure.com:443/"
key = 'y5ZatCRxHYVOmYkBpwfP1nJV9yiR5zzyULXetVwZlG97CRUvQ46hfIXg9e9Nlv84aR0742L1YoIMao11NB8GmA=='
client = CosmosClient(endpoint, key)
database_name = "dairyDB"
database = client.create_database_if_not_exists(id=database_name)
container_name = "weather"
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)


app = Flask(__name__)


@app.route("/weather")
def members():
    #query = """SELECT c.datesql, c.Animal_ID, c.Group_ID, c.AnimalStatus, c.Gynecology_Status, c["Activity(steps/hr)"], c["Weight(gr)"], c["Yield(gr)"] FROM c WHERE c.Animal_ID = 1"""
    query = """SELECT c.Date, c.highest_temp, c.lowest_temp, c.avg_temp, c.highest_thi, c.lowest_thi, c.avg_thi, c.num_records_on_day FROM c"""
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    return {"cows": items}


if __name__ == "__main__":
    app.run(debug=True)
