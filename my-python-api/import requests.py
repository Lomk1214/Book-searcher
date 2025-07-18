from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_book_and_similar_link(book_name):
    # Optional: Headless mode if you don't want the browser to open
    options = Options()
    options.add_argument("--headless")  # Remove this line if you want to see the browser
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")  # Suppress logging

    driver = webdriver.Chrome(options=options)  # Or provide path to chromedriver
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Search for the book
        search_url = f"https://www.goodreads.com/search?q={book_name}"
        print(f"Searching: {search_url}")
        driver.get(search_url)

        # Click the first book link
        first_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'bookTitle')))
        first_link.click()

        # Step 2: Scrape title, author, and cover
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Text__title1')))
        title = driver.find_element(By.CLASS_NAME, 'Text__title1').text.strip()

        try:
            author = driver.find_element(By.CLASS_NAME, 'ContributorLink').text.strip()
        except:
            author = "N/A"

        try:
            img = driver.find_element(By.CSS_SELECTOR, 'img.ResponsiveImage')
            image_url = img.get_attribute('src')
        except:
            image_url = "N/A"

        print(f"\nTitle: {title}")
        print(f"Author: {author}")
        print(f"Cover: {image_url}")

        # Step 3: Find the "All similar books" button
        time.sleep(1)  # Allow content below fold to load (optional)
        try:
            similar_button = wait.until(EC.presence_of_element_located((
                By.XPATH, '//a[.//span[contains(text(), "All similar books")]]'
            )))
            similar_url = similar_button.get_attribute('href')
            print(f"Similar books page: {similar_url}")
        except:
            print("Similar books link not found.")

    finally:
        driver.quit()


get_book_and_similar_link("Unbroken")
