from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from books.models import Book

def scrape_books():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://books.toscrape.com/")

    items = driver.find_elements(By.CLASS_NAME, "product_pod")

    for item in items[:5]:
        link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

        # open each book page
        driver.get(link)

        title = driver.find_element(By.TAG_NAME, "h1").text

        try:
            description = driver.find_element(By.ID, "product_description").find_element(By.XPATH, "following-sibling::p").text
        except:
            description = "No description"

        Book.objects.get_or_create(
            title=title,
            defaults={
                "author": "Unknown",
                "description": description,
                "rating": 0,
                "url": link
            }
        )

        driver.back()

    driver.quit()