import getClubData

import csv

def makeTabs():
    Index, titles, categories, missionDescripts, presidentNames, emails, pictureUrls = getClubData.getData()

    tags = {
        'difficulty': ['beginner', 'intermediate', 'advanced'],
        'category': ['academic', 'social', 'sports', 'arts', 'technology', 'community service'],
        'participation': ['in-person', 'virtual', 'hybrid'],
        'commitment_level': ['casual', 'regular', 'competitive'],
        'membership_type': ['open to all', 'invite-only', 'application required'],
        'focus_area': ['leadership', 'networking', 'skill-building', 'recreational'],
        'schedule': ['weekly', 'bi-weekly', 'monthly', 'project-based'],
        'benefits': ['certification', 'mentorship', 'career opportunities', 'scholarship eligibility']
    }

    fieldnames = ['title']
    for tag_type, values in tags.items():
        for val in values:
            fieldnames.append(f"{tag_type}_{val.replace(' ', '_')}")  

    fieldnames += ['numRatings', 'rated']

    with open('./data/club_tag_counts.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        def zero_tag_counts():
            return {f"{tag_type}_{val.replace(' ', '_')}": 0 for tag_type in tags for val in tags[tag_type]}

        for title in titles:
            row = {'title': title}
            tag_counts = zero_tag_counts()

            tag_counts['difficulty_beginner'] = 5
            tag_counts['difficulty_intermediate'] = 2
            tag_counts['category_academic'] = 3
            tag_counts['category_technology'] = 1
            tag_counts['participation_in-person'] = 4
            tag_counts['commitment_level_regular'] = 4
            tag_counts['membership_type_open_to_all'] = 6
            tag_counts['focus_area_skill-building'] = 2
            tag_counts['schedule_weekly'] = 3
            tag_counts['benefits_career_opportunities'] = 2

            num_ratings = sum(tag_counts.values())
            row['numRatings'] = num_ratings
            row['rated'] = 5
            row.update(tag_counts)
            writer.writerow(row)

makeTabs()