import json

def getCourses():
    with open("./data/courses.json", "r") as f:
        data = json.load(f)

    prefixes = []
    numbers = []
    titles = []
    descriptions = []
    jsonStrings = []
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
        jsonStrings.append("{Prefix: \'" + prefix + "\',Number: \'" + number + "\',Title: " + title + "\'Description: \'" + description + "\'}")

    return jsonStrings