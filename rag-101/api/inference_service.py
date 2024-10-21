from elasticsearch import Elasticsearch
import os

ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")



# TODO move this to central location so this and search_service don't create separate connections
# Initialize the Elasticsearch client
es_client = Elasticsearch(
    hosts=os.getenv('ES_URL', 'http://kubernetes-vm:9200'),
    # api_key=os.getenv('ES_API_KEY'),
    basic_auth=(
        os.getenv('ES_USER', 'elastic'),
        os.getenv('ES_PASSWORD', 'changeme')
    ),
    timeout=90
)


def es_chat_completion(prompt, inference_id):

    response = es_client.inference.inference(
        inference_id = inference_id,
        task_type = "completion",
        input = prompt,
        timeout="90s"
    )


    return response['completion'][0]['result']



