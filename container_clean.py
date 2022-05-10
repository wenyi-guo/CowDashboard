from azure.cosmos import exceptions, CosmosClient, PartitionKey
import argparse

endpoint = "https://diaryinstance.documents.azure.com:443/"

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('type', type=str, help='container type')
args = parser.parse_args()

key = 'y5ZatCRxHYVOmYkBpwfP1nJV9yiR5zzyULXetVwZlG97CRUvQ46hfIXg9e9Nlv84aR0742L1YoIMao11NB8GmA=='
client = CosmosClient(endpoint, key)
database_name = "dairyTemp"
database = client.create_database_if_not_exists(id=database_name)

weather_container = database.create_container_if_not_exists(
    id="weather_temp",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
milk_container = database.create_container_if_not_exists(
    id="milk_temp",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
rum_container = database.create_container_if_not_exists(
    id="rum_temp",
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

query =  """SELECT * FROM c"""
if args.type=="rum": 
        container = rum_container
elif args.type=="milk":
        container = milk_container
elif args.type=="weather":
        container = weather_container
else:
    print("container don't exist")
    exit(0) 

for item in container.query_items( query=query,enable_cross_partition_query=True):
    container.delete_item(item, partition_key=item['id'])
