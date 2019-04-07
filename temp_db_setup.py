"""
A file for creating a temporary SQLite database.
"""

import sqlite3
conn = sqlite3.connect('jobscrape.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS posting_data;')
c.execute('CREATE TABLE posting_data (Hyperlink string, Posting string);')

conn.commit()
conn.close()