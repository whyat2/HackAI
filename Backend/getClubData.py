import pandas as pd

def getData():
    dataframe = pd.read_csv("./data/Student Organization Directory.csv")

    Index = []
    title = []
    category = []
    missionDescripts = []
    presidentName = []
    email = []
    pictureUrl = []

    for index, row in dataframe.iterrows():
        title.append(row['Title'])
        category.append(row['Category'])
        missionDescripts.append(row["Mission, Purpose, and Organization Description"])
        presidentName.append(row["President's Full Name"])
        email.append(row["Contact Information Email"])
        pictureUrl.append(row["Picture"])
        Index.append(index)

    return Index, title, category, missionDescripts, presidentName, email, pictureUrl

def printAllInfo(Index, title, category, missionDescripts, presidentName, email, pictureUrl):
    for i in range(len(Index)):
        print(f"Index: {Index[i]}")
        print(f"Title: {title[i]}")
        print(f"Category: {category[i]}")
        print(f"Mission Description: {missionDescripts[i]}")
        print(f"President's Name: {presidentName[i]}")
        print(f"Email: {email[i]}")
        print(f"Picture URL: {pictureUrl[i]}")
        print("-" * 40)

def printAllWithA(index, title, category, missionDescripts, presidentName, email, pictureUrl):
    for i in range(len(Index)):
        if title[i].lower().startswith('a'):
            print(f"Index: {Index[i]}")
            print(f"Title: {title[i]}")
            print(f"Category: {category[i]}")
            print(f"Mission Description: {missionDescripts[i]}")
            print(f"President's Name: {presidentName[i]}")
            print(f"Email: {email[i]}")
            print(f"Picture URL: {pictureUrl[i]}")
            print("-" * 40)


def getEmbeddingString(index, title, category, missionDescripts):
    EmbeddingStrings = []
    for i in range(len(index)):
        #EmbeddingStrings.append("{Title: " + title[i] + "@$%,Category: " + category[i] + "!$%,Mission Description: " + missionDescripts[i] + "&$%}")
        EmbeddingStrings.append(title[i] + "$$$" + category[i] + "$$$" + missionDescripts[i] + "@#")
    return EmbeddingStrings


Index, title, category, missionDescripts, presidentName, email, pictureUrl = getData()
printAllWithA(Index, title, category, missionDescripts, presidentName, email, pictureUrl)
print(getEmbeddingString(Index, title, category, missionDescripts))