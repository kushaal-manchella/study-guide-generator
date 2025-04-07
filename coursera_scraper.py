# coursera_scraper.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

COURSERA_EMAIL = os.getenv("COURSERA_EMAIL")
COURSERA_PASSWORD = os.getenv("COURSERA_PASSWORD")

def get_formatted_html_source():
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    pretty_html = soup.prettify() 
    return pretty_html



def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def login_to_coursera(driver):
    driver.get("https://www.coursera.org/login")

    try:
        email_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-e2e='login-email-input']"))
        )
        email_input.send_keys(os.getenv("COURSERA_EMAIL"))
        print("✅ Email field found and filled.")
        email_input.send_keys(Keys.TAB)  # triggers blur event
    except:
        print("❌ Could not find email input.")
        with open("debug_email.html", "w", encoding="utf-8") as f:
            f.write(get_formatted_html_source())
        raise

    try:
        password_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-e2e='login-password-input']"))
        )
        password_input.send_keys(os.getenv("COURSERA_PASSWORD"))
        password_input.send_keys(Keys.RETURN)
        print("✅ Password field found and submitted.")
    except:
        print("❌ Could not find password input.")
        with open("debug_password.html", "w") as f:
            f.write(get_formatted_html_source())
        raise

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rc-DomainNav"))
    )
    print("✅ Successfully logged in.")





# TODO: Implement course navigation and material scraping
def scrape_course_materials(driver, course_slug):
    course_url = f"https://www.coursera.org/learn/{course_slug}/home/welcome"
    driver.get(course_url)
    time.sleep(5)  # Allow time for course content to load
    print(f"Opened course page: {course_url}")

    # TODO: Parse weekly sections and download transcripts/slides


if __name__ == "__main__":
    course_slug = input("Enter Coursera course slug (e.g., neural-networks-deep-learning): ")
    driver = setup_driver()
    try:
        login_to_coursera(driver)
        scrape_course_materials(driver, course_slug)
    finally:
        driver.quit()
