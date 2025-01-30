from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from elasticsearch import helpers, Elasticsearch
import argparse


parser = argparse.ArgumentParser()
# required args
parser.add_argument("--es_password", dest="es_password", required=True)
parser.add_argument("--es_url", dest="es_url", required=True)
args = parser.parse_args()
client = Elasticsearch(
    hosts=[args.es_url], 
    basic_auth=('elastic', args.es_password),
    request_timeout=600,
)

client = client.options(request_timeout=60)

# Using langchain for splitting and indexing
def index_pdf_using_langchain(pdf_url, index_name):
    loader = PyPDFLoader(pdf_url)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=256
    )
    docs = loader.load_and_split(text_splitter=text_splitter)

    actions = [
        {
            "_index": index_name,
            "_source": {
                "text": doc.page_content,
                "page_number": i,
            },
        }
        for i, doc in enumerate(docs)
    ]

    # Use the bulk helper to index documents
    helpers.bulk(client, actions)
    print(f"Indexed {len(docs)} chunks into Elasticsearch index: {index_name}")

# Main processing logic
def main():
    pdf_url = "https://arxiv.org/pdf/2103.15348.pdf"
    # Then, using langchain for splitting and indexing
    index_pdf_using_langchain(pdf_url, "elser_index")

if __name__ == "__main__":
    main()
