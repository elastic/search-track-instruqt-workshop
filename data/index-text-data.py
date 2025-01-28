import PyPDF2
import requests
from io import BytesIO
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


client = client.options(request_timeout=60)

# Function to download a PDF from a URL
def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print("Failed to download PDF")
    return None

# Function to extract text from PDF pages
def get_pdf_pages(pdf_file):
    pages = []
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text = page.extract_text()
        pages.append(text)
    return pages

# Function to index PDF pages into Elasticsearch
def index_pdf_to_elasticsearch(pages, index_name):
    actions = [
        {
            "_index": index_name,
            "_source": {
                "text": page,
                "page_number": i,
            },
        }
        for i, page in enumerate(pages)
    ]

    # Use the bulk helper with the updated client
    helpers.bulk(
        client,
        actions,
    )
    print(f"Indexed {len(pages)} pages into Elasticsearch index: {index_name}")

# Main processing logic
def main():
    pdf_url = "https://arxiv.org/pdf/2103.15348.pdf"
    pdf_file = download_pdf(pdf_url)
    
    if pdf_file:
        pages = get_pdf_pages(pdf_file)
        index_pdf_to_elasticsearch(pages, "my_pdf_index_bm25")

if __name__ == "__main__":
    main()
