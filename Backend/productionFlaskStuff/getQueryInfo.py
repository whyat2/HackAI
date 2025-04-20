import numpy as np
from dotenv import load_dotenv
import os
import chromadb
import google.generativeai as genai
import google.generativeai as genai
from google.api_core import retry

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
chromaClient = chromadb.PersistentClient()
embedClubsCollection = chromaClient.get_collection(name="embeddedClubs")
retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}

def getQueryResults(Input):
    Input = [Input]
    InputEmbedding = genai.embed_content(
                model="models/text-embedding-004",
                content=Input,
                task_type='RETRIEVAL_QUERY',
                request_options=retry_policy
    )
    results = embedClubsCollection.query(
        query_embeddings=InputEmbedding["embedding"],
        n_results=50
    )
    print(results)
    documents = results.get("documents", [])
    print(documents)
    for doc_list in documents:
        return doc_list
