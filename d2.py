import requests
from bs4 import BeautifulSoup
from bs4.element import Comment


import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("data.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table (if it doesn't exist)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY,
        url TEXT,
        text TEXT
    )
"""
)


url = "https://www.destinypedia.com"

# Make a request to the URL
response = requests.get(url + "/Category:Characters")

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the sublinks
sublinks = soup.find_all("a")


def tag_visible(element):
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def generate_scraping_bot(sublink_url):
    print(url + sublink_url)
    response = requests.get(url + sublink_url)
    soup = BeautifulSoup(response.content, "html.parser")
    # body_text = soup.body.get_text()
    # return body_text
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


# exception_list of not useful links
exception_list = [
    "https://www.destinypedia.com/Special:CreateAccount",
    "https://www.destinypedia.com/Special:UserLogin",
]


# Generate a scraping bot for each sublink
for sublink in sublinks[90:100]:
    sublink_url = sublink["href"]
    if sublink_url in exception_list:
        pass
    try:
        scraped_text = generate_scraping_bot(sublink_url)
        cursor.execute(
            "INSERT INTO data (url, text) VALUES (?, ?)", (sublink_url, scraped_text)
        )
    except:
        pass


# Commit the changes
conn.commit()

# Close the connection
conn.close()
