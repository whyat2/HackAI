import csv

csv_file_path = "./data/club_tag_counts.csv"
import csv

def getBestTagsForClubsWithRating(titles):
    tag_definitions = {
        'difficulty': ['beginner', 'intermediate', 'advanced'],
        'category': ['academic', 'social', 'sports', 'arts', 'technology', 'community service'],
        'participation': ['in-person', 'virtual', 'hybrid'],
        'commitmentLevel': ['casual', 'regular', 'competitive'],
        'membershipType': ['open to all', 'invite-only', 'application required'],
        'focusArea': ['leadership', 'networking', 'skill-building', 'recreational'],
        'schedule': ['weekly', 'bi-weekly', 'monthly', 'project-based'],
        'benefits': ['certification', 'mentorship', 'career opportunities', 'scholarship eligibility']
    }

    results = []
    titles_lower = [t.lower().strip() for t in titles]

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            row_title = row['title'].strip().lower()
            if row_title in titles_lower:
                best_tags = {'title': row['title']}

                # Find the best tag for each category
                for tag_type, options in tag_definitions.items():
                    best_option = None
                    max_count = -1
                    for option in options:
                        col_name = f"{tag_type}{option.capitalize()}"
                        count = int(row.get(col_name, 0))
                        if count > max_count:
                            max_count = count
                            best_option = option
                    best_tags[tag_type] = best_option

                # Add numRatings and rated
                best_tags['numRatings'] = int(row.get('numRatings', 0))
                best_tags['rated'] = int(row.get('rated', 0))

                results.append(best_tags)

    return results

def parseForTags(inputString):
    titles = []
    for clubStr in inputString:
        parseClubString = clubStr.split("$$$")
        titleMatch = parseClubString[0]
        bestStuff = getBestTagsForClubsWithRating([titleMatch])
        
        titles.append(titleMatch)
    return titles
import getQueryInfo
print(getBestTagsForClubsWithRating(parseForTags(getQueryInfo.getQueryResults("MachineLearning"))))
#print(getBestTagsForClubsWithRating(["AWS Cloud Club", "Banking & Capital Markets Workshop"]))