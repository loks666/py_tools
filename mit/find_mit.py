import requests
from bs4 import BeautifulSoup
import time
import csv

BASE_URL = "https://bcs.mit.edu"
FACULTY_URL = "https://bcs.mit.edu/faculty"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def get_faculty_profiles():
    response = requests.get(FACULTY_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    faculty_links = []
    for div in soup.find_all('div', class_='faculty-link'):
        link_tag = div.find('a')
        if link_tag and 'href' in link_tag.attrs:
            faculty_links.append(BASE_URL + link_tag['href'])

    return faculty_links


def get_faculty_details(profile_url):
    response = requests.get(profile_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    contact_div = soup.find('div', class_='person-contact')
    faculty_info = {"URL": profile_url, "Email": "", "Phone": "", "Lab Website": "", "Admin Asst": ""}

    if contact_div:
        email_div = contact_div.find('div', class_='field--name-field-email')
        if email_div:
            faculty_info["Email"] = email_div.find('a').text.strip()

        phone_div = contact_div.find('div', class_='field--name-field-phone')
        if phone_div:
            faculty_info["Phone"] = phone_div.find('div', class_='field__item').text.strip()

        website_div = contact_div.find('div', class_='website-link')
        if website_div:
            faculty_info["Lab Website"] = website_div.find('a')['href'].strip()

        admin_div = contact_div.find('div', class_='field--name-field-administrative-asst')
        if admin_div:
            faculty_info["Admin Asst"] = admin_div.find('div', class_='field__item').text.strip()

    return faculty_info


def main():
    faculty_profiles = get_faculty_profiles()
    faculty_data = []

    print(f"Found {len(faculty_profiles)} faculty profiles. Fetching details...")
    for profile in faculty_profiles:
        try:
            details = get_faculty_details(profile)
            faculty_data.append(details)
            print(f"Scraped: {details}")
            time.sleep(1)  # Avoid overwhelming the server
        except Exception as e:
            print(f"Error scraping {profile}: {e}")

    with open("mit_faculty_contacts.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["URL", "Email", "Phone", "Lab Website", "Admin Asst"])
        writer.writeheader()
        writer.writerows(faculty_data)

    print("Data saved to mit_faculty_contacts.csv")


if __name__ == "__main__":
    main()
