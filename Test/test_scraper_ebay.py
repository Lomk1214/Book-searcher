import requests
import undetected_chromedriver as uc

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def search_goodreads(book_title):
    query = '+'.join(book_title.strip().split())
    url = f"https://www.goodreads.com/search?q={query}&search_type=books"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    first_row = soup.select_one("table.tableList tr")
    if not first_row:
        print("No book found.")
        return

    title_elem = first_row.select_one("a.bookTitle span")
    author_elem = first_row.select_one("a.authorName span")
    link_elem = first_row.select_one("a.bookTitle")

    if not title_elem or not author_elem or not link_elem:
        print("Missing expected content in result row.")
        return

    title = title_elem.text.strip()
    author = author_elem.text.strip()
    link = "https://www.goodreads.com" + link_elem['href']

    print("📚 Goodreads Result:")
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Link: {link}")


def search_imdb(show_title):
    query = '+'.join(show_title.strip().split())
    url = f"https://www.imdb.com/find?q={query}&s=tt"

    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options, headless=True)
    
    try:
        driver.get(url)

        # Wait up to 10 seconds for results to appear
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".findList .findResult")))

        # Screenshot for verification (optional)
        driver.save_screenshot("imdb_search.png")

        # Now safely get results
        results = driver.find_elements(By.CSS_SELECTOR, ".findList .findResult")
        print(f"Found {len(results)} results")
        if not results:
            print("No results found.")
            return
        
        first_result = results[0]
        title_elem = first_result.find_element(By.CSS_SELECTOR, "td.result_text a")
        title = title_elem.text
        link = title_elem.get_attribute("href")

        print("🎬 IMDb Result:")
        print(f"Title: {title}")
        print(f"Link: {link}")

    finally:
        driver.quit()


search_goodreads("The Great Gatsby")
search_imdb("Inception")

# def search_imdb(show_title):
#     query = '+'.join(show_title.strip().split())
#     url = f"https://www.imdb.com/find?q={query}&s=tt"

#     service = Service()
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless=new")  # More stable headless mode
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")
#     driver = webdriver.Chrome(service=service, options=options)

#     try:
#         driver.get(url)
#         driver.save_screenshot("imdb_search.png")  # Save screenshot for debugging
#         import time
#         time.sleep(2)  # give the page time to render JS

#         # Grab all results
#         results = driver.find_elements(By.CSS_SELECTOR, ".findList .findResult")
#         print(f"Found {len(results)} results")
#         if not results:
#             print("No results found.")
#             return

#         # Use the first result
#         first_result = results[0]
#         title_elem = first_result.find_element(By.CSS_SELECTOR, "td.result_text a")
#         title = title_elem.text
#         link = title_elem.get_attribute("href")

#         print("🎬 IMDb Result:")
#         print(f"Title: {title}")
#         print(f"Link: {link}")

#     except Exception as e:
#         import traceback
#         print("Error occurred:")
#         traceback.print_exc()
#     finally:
#         driver.quit()








# import requests
# from bs4 import BeautifulSoup

# url = "https://example.com"
# headers = {"User_Agent": "Mozilla/5.0"}

# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.content, "lxml")

# print(soup.title.text)

# import requests
# from bs4 import BeautifulSoup

# # Define a function that accepts a search term (like "laptop")
# def scrape_ebay(search_term):

# # Replace spaces with "+" so it works in the eBay search URL
#     search_term = search_term.replace(" ", "+")
#     url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}"

# # Headers help pretend you're a browser (so websites don’t block you as a bot)
#     headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/114.0.0.0 Safari/537.36"
#     }

# # Send a GET request to the URL with headers
#     response = requests.get(url, headers=headers)

# # Check if the request was successful (status code 200 means OK)
#     if response.status_code != 200:
#         print("Failed to fetch the page")
#         print("Status Code:", response.status_code)
#         print("response Headers:", response.headers)
#         # print("response Content:", response.content[:200])
#         return

#  # Parse the page content (HTML) using BeautifulSoup with the "lxml" parser
#     soup = BeautifulSoup(response.content, "lxml")

# # Select all search result items on the page using CSS selectors
#     items = soup.select(".s-item")

# # Loop through the first 10 items only (to avoid overwhelming output)
#     for item in items [:10]:
#     # Try to find the product title inside each item block
#         title = item.select_one(".s-item__title")
#     # Try to find the product price
#         price = item.select_one(".s-item__price")
#     # Try to find the link to the product page
#         link = item.select_one('.s-item__link')
#     # Only print the result if all parts (title, price, link) were found
#         if title and price and link:
#             print("Title:", title.text)     # Print the product title
#             print("Price:", price.text)     # Print the product price
#             print("Link:", link["href"])    # Print the link to the product
#             print("-" * 50)                 # Print the link to the produc

# # Call the function to run the scraper for a test search
# scrape_ebay("wireless earbuds")
# import selenium

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# def scrape_ebay(search_term):

#     # replace spaces with "+" for the eBay search URL
#     search_term = search_term.replace(" ", "+")
#     url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}"

#     # set up the selenium driver with Chrome
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")  # start browser maximized
#     options.add_argument("--disable-blink-features=AutomationControlled")  # avoid detection
#     options.add_argument("--headless")  # run in headless mode (no GUI), # Run in background (remove to see browser)

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     driver.get(url)  # open the eBay search page

#     time.sleep(3)  # wait for the page to load (you can adjust this)

#     items= driver.find_elements(By.CSS_SELECTOR, ".s-item")[:10]  # find all search result items

#     for item in items:
#         try:
#             title = item.find_element(By.CSS_SELECTOR, ".s-item__title").text  # get the product title
#             price = item.find_element(By.CSS_SELECTOR, ".s-item__price").text  # get the product price
#             link = item.find_element(By.CSS_SELECTOR, ".s-item__link").get_attribute("href")  # get the product link

#             print("Title:", title)  # print the product title
#             print("Price:", price)  # print the product price
#             print("Link:", link)  # print the link to the product
#             print("-" * 50)  # separator line

#         except Exception as e:
#             continue

#     driver.quit()  # call the function to run the scraper

# def scrape_walmart(search_term):

#     #replace spaces with "+" for the Walmart search URL
#     search_term = search_term.replace(" ", "+")
#     url = f"https://www.walmart.com/search/?query={search_term}"
#     # url = f"https://www.walmart.com/search?q={search_term}"

#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-blink-features=AutomationControlled")  # avoid detection
#     # options.add_argument("--headless")  # run in headless mode (no GUI), # Run in background (remove to see browser)

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get(url)  # open the Walmart search page

#     time.sleep(5)

#     items = driver.find_elements(By.CSS_SELECTOR, "div[data-type='items'] div[data-item-id]")[:10]

#     for item in items:
#         try:
# # top comment was chats suggestion. We'll see what works best

#             # title = item.find_element(By.CSS_SELECTOR, "a span.lh-title").text 
#             # price = item.find_element(By.CSS_SELECTOR, "span[data-automation-id='product-price']").text
#             # link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

#             title = item.find_element(By.CSS_SELECTOR, "span[data-automation='product-title']").text  # get the product title
#             price = item.find_element(By.CSS_SELECTOR, "span[data-automation='price']").text  # get the product price
#             link = item.find_element(By.CSS_SELECTOR, "a[data-automation='product-link']").get_attribute("href")  # get the product link

#             print("Title:", title)  # print the product title
#             print("Price:", price)  # print the product price
#             print("Link:", link)  # print the link to the product
#             print("-" * 50)
#         except Exception:
#             continue

#     driver.quit()



# def scrape_target(search_term):

#     search_term = search_term.replace(" ", "%20")
#     url = f"https://www.target.com/s?searchTerm={search_term}"

#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-blink-features=AutomationControlled")  # avoid detection

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get(url)  # open the Target search page

#     try:
#         WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test='product-card'"))
#         )
        
#         items = driver.find_elements(By.CSS_SELECTOR, "div[data-test='product-card'")[:11]  # find all search result items
        
#         if not items:
#             print("No items found. Please check the search term or try again later.")
#             return
        
#         for item in items:
#             try:
#                 title = item.find_element(By.CSS_SELECTOR, "a[data-test='product-title']").text
#                 price = item.find_element(By.CSS_SELECTOR, "div[data-test='current-price']").text
#                 link = item.find_element(By.CSS_SELECTOR, "a[data-test='product-title']").get_attribute("href")

#                 print("Title:", title)  # print the product title
#                 print("Price:", price)  # print the product price
#                 print("Link:", "https://www.target.com" + link)  # print the link to the product
#                 print("-" * 50)  # separator line

#             except Exception as e:
#                 print("Error parsing an item:", e)
#                 continue
            
#     except Exception as e:
#         print("Error loading items:", e)

#     driver.quit()  # close the browser

# scrape_target("Earbuds")