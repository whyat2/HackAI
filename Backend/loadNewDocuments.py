import json
import getClubData
import chromadb
index, title, category, missionDescripts, presidentName, email, pictureUrl = getClubData.getData()
embedStrings = getClubData.getEmbeddingString(index, title, category, missionDescripts)
with open("./data/club_embeddings.json", "r") as f:
    data = json.load(f)
clubEmbedding = data.get("embedding")
chromaClient = chromadb.PersistentClient()
chromaClient.delete_collection("embeddedClubs")
embedClubsCollection = chromaClient.get_or_create_collection(name="embeddedClubs")
embedClubsCollection.add(
    documents=embedStrings,
    ids=[str(i) for i in index],
    embeddings=clubEmbedding
)
print(embedClubsCollection.count())