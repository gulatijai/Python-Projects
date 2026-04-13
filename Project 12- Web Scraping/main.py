from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

chrome_options= webdriver.ChromeOptions()
driver= webdriver.Chrome(options= chrome_options)

with open('book.csv','w', newline='', encoding='utf-8') as file:
    writer= csv.writer(file)
    writer.writerow(['Title', 'Price', 'Rating', 'Availability'])

    for page in range(1,10):
        url= f"https://books.toscrape.com/catalogue/page-{page}.html"
        driver.get(url)
        print(f"Scraping page {page}...")
        time.sleep(2)

        books= driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        print(f"Found {len(books)} books on page {page}")

        for book in books:
            title= book.find_element(By.CSS_SELECTOR,'h3 a').get_attribute("title")
            price= book.find_element(By.CSS_SELECTOR, '.price_color').text
            rating=book.find_element(By.CSS_SELECTOR, '.star-rating').get_attribute("class")
            rating= rating.replace("star-rating","")
            availability= book.find_element(By.CSS_SELECTOR,'.availability').text.strip()
            writer.writerow([title, price, rating, availability])
            print(f"Title: {title} | Price: {price} | Rating: {rating} | Availability: {availability}")

print("Scraping complete!")
driver.quit()