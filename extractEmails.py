from pathlib import Path
import re
import requests
import mysql.connector
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}

OUTPUT_FILE = "emails_found.txt"


def get_websites_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cessi",
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, website
        FROM main
        WHERE website IS NOT NULL
        AND website <> ''
        AND email IS NULL
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def extract_emails_from_text(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    emails = re.findall(pattern, text)

    ignored = [
        ".png",
        ".jpg",
        ".jpeg",
        ".svg",
        ".webp",
        "example.com",
    ]

    clean_emails = []

    for email in emails:
        email = email.strip().lower()

        if any(ignore in email for ignore in ignored):
            continue

        clean_emails.append(email)

    return list(set(clean_emails))


def get_emails_from_website(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True,
        )

        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator=" ")

        emails = extract_emails_from_text(text)

        # Recherche des mailto:
        for link in soup.find_all("a", href=True):
            href = link["href"]

            if "mailto:" in href:
                email = href.replace("mailto:", "").split("?")[0]
                emails.append(email.lower())

        return list(set(emails))

    except Exception as error:
        print(f"[ERROR] {url} -> {error}")
        return []


def save_result(website, emails):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
        file.write(f"Website: {website}\n")

        if emails:
            for email in emails:
                file.write(f"  - {email}\n")
        else:
            file.write("  - No email found\n")

        file.write("\n")


def process():
    websites = get_websites_from_db()

    # reset file
    open(OUTPUT_FILE, "w", encoding="utf-8").close()

    for row in websites:
        website = row[1]

        print(f"\n[CHECKING] {website}")

        emails = get_emails_from_website(website)

        if emails:
            print(f"[FOUND] {len(emails)} email(s)")
        else:
            print("[NO EMAIL FOUND]")

        save_result(website, emails)

    print(f"\nResults saved in: {OUTPUT_FILE}")


if __name__ == "__main__":
    process()