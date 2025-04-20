import json

FILEPATH = "./data/courses.json"

subject = []
course_number = []
title = []
description = []

with open(FILEPATH, 'r') as file:
    data = json.load(file)

for course in data:
    subject = course.get("subject_prefix")
    course_number = course.get("course_number")
    title = course.get("title")
    description = course.get("description")

    print(f"Subject: {subject}")
    print(f"Course Number: {course_number}")
    print(f"Title: {title}")
    print(f"Description: {description}")