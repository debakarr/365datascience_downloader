import json
import urllib
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from download_single_course import download_course, download_course_resource

if __name__ == "__main__":
    base_url = "https://365datascience.com/"
    courses_collector_url = urllib.parse.urljoin(base_url, "courses")

    page = requests.get(courses_collector_url)
    soup = BeautifulSoup(page.content, "html.parser")

    courses = soup.find_all("div", class_="course-card-body")
    all_course_link = [urllib.parse.urljoin(base_url, course.a["href"]) for course in courses]

    input_file = Path(__file__).parent / "input.json"
    input_data = json.loads(input_file.read_text())
    authorization_token = input_data.get("authorization_token")
    policy_key = input_data.get("policy_key")
    quality = input_data.get("quality")

    for course_url in all_course_link:
        download_course_resource(course_url=course_url, authorization_token=authorization_token)
        download_course(
            course_url=course_url, authorization_token=authorization_token, policy_key=policy_key, quality=quality
        )
