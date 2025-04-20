import numpy as np
from dotenv import load_dotenv
import os
import chromadb
import google.generativeai as genai
import google.generativeai as genai
from google.api_core import retry
import json
import urllib
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
chromaClient = chromadb.PersistentClient()
embedClubsCollection = chromaClient.get_collection(name="embeddedClubs")
retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}
with open("./data/courses.json", "r") as f:
    data = json.load(f)


prefixes = []
numbers = []
titles = []
descriptions = []
unique_prefixes = []
unique_numbers = []
unique_titles = []
unique_descriptions = []
# Extract and print course details
for course in data:
    prefix = course.get("subject_prefix", "N/A")
    number = course.get("course_number", "N/A")
    #if prefix not in prefixes or number not in numbers:
    title = course.get("title", "N/A")
    description = course.get("description", "N/A")
    prefixes.append(prefix)
    numbers.append(number)
    titles.append(title)
    descriptions.append(description)


seen = set()
for prefix, number, title, description in zip(prefixes, numbers, titles, descriptions):
    key = (prefix, number)
    if key not in seen:
        seen.add(key)
        unique_prefixes.append(prefix)
        unique_numbers.append(number)
        unique_titles.append(title)
        unique_descriptions.append(description)

def getCourses(courseString):
    print(courseString)
    getData = courseString.split(" ")
    prefix = getData[0]
    numbers = getData[1]
    print(prefix)
    for i in range(0, len(unique_prefixes)):
        if unique_prefixes[i] == prefix and unique_numbers[i] == numbers:
            return unique_titles[i], unique_descriptions[i]

def getCourseQuery(Input):
    Input = Input[1:-1]
    title, description = getCourses(Input)
    embedString = "Course Code: " + Input + "Course Title: " + title + "Course Description: " + description
    InputEmbedding = genai.embed_content(
                model="models/text-embedding-004",
                content=embedString,
                task_type='RETRIEVAL_QUERY',
                request_options=retry_policy
    )
    results = embedClubsCollection.query(
        query_embeddings=InputEmbedding["embedding"],
        n_results=50
    )
    #print(results)
    documents = results.get("documents", [])
    #print(documents)
    for doc_list in documents:
        return doc_list

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
    documents = results.get("documents", [])
    #print(documents)
    for doc_list in documents:
        return doc_list


#print(getCourseQuery("CS 2336"))