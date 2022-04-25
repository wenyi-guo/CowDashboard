from flask import Flask
from azure.cosmos import exceptions, CosmosClient, PartitionKey

endpoint = "https://diaryinstance.documents.azure.com:443/"
key = 'y5ZatCRxHYVOmYkBpwfP1nJV9yiR5zzyULXetVwZlG97CRUvQ46hfIXg9e9Nlv84aR0742L1YoIMao11NB8GmA=='
client = CosmosClient(endpoint, key)
database_name = "daily_milk"
database = client.create_database_if_not_exists(id=database_name)
container_name = "container 1"
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/Animal_ID"),
    offer_throughput=400
)


app = Flask(__name__)


@app.route("/members")
def members():
    query = """SELECT c.datesql, c.Animal_ID, c.Group_ID, c.AnimalStatus, c.Gynecology_Status, c["Activity(steps/hr)"], c["Weight(gr)"], c["Yield(gr)"] FROM c WHERE c.Animal_ID = 1"""

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    return {"cows": items}


if __name__ == "__main__":
    app.run(debug=True)
