Welcome to the Club Hub!

A friendly, up-to-date website for UTD student organizations! Find your next cozy hangout, fun night out, professional experience, or all of the above here at the Club Hub.

## Inspiration
Have you ever tried to look for student orgs at UTD? After wrestling with our school website's infamous 400 entry spreadsheet, you'll soon find out most students find their clubs through either sheer chance or word of mouth. To streamline this process, we introduce the Club Hub: a one stop website for all your club searches.

## What it does
Club Hub allows you to search for any club that's registered with the school database. The club description includes their mission statement and contact information. Interested in learning more from a class topic or translating it into practical experience? Search for a course name to find relevant clubs!

## How we built it
We used a chromadb's open source RAG system with Gemini embeddings to encode all of the club data from given CSV & Json files. We then queried this data also using Gemini embeddings to return the best semantic matches for each query.

* Languages: Python, Javascript, HTML, CSS
* Library: React
* Environment: Node.js
* Framework: Flask
* Data: Nebula Labs, UTD 

## Coming up for Club Hub
* User login
* Favorite club list
* Upload club information form for officers
* Club calendar & scheduler
