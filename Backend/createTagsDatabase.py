import sqlite3

conn = sqlite3.connect("./data/tags.db")  
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE clubs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    difficulty TEXT CHECK(difficulty IN ('beginner', 'intermediate', 'advanced')),
    category TEXT CHECK(category IN ('academic', 'social', 'sports', 'arts', 'technology', 'community service')),
    participation TEXT CHECK(participation IN ('in-person', 'virtual', 'hybrid')),
    commitment_level TEXT CHECK(commitment_level IN ('casual', 'regular', 'competitive')),
    membership_type TEXT CHECK(membership_type IN ('open to all', 'invite-only', 'application required')),
    focus_area TEXT CHECK(focus_area IN ('leadership', 'networking', 'skill-building', 'recreational')),
    schedule TEXT CHECK(schedule IN ('weekly', 'bi-weekly', 'monthly', 'project-based')),
    benefits TEXT CHECK(benefits IN ('certification', 'mentorship', 'career opportunities', 'scholarship eligibility'))
);
""")

