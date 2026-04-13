from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import openpyxl

# setup
options= webdriver.ChromeOptions()
driver= webdriver.Chrome(options=options)

#setup excel
wb= openpyxl.Workbook()
ws= wb.active
ws.title="Laminex Documents"
ws.append(['Document Name', 'Brand', 'Document Type', 'Date Issued'])

BASE_URL = "https://www.laminex.com.au/document-library?q=%3Atitle-asc%3AsearchCategory%3ADOCUMENT%3AuserTypes%3AFOR-YOUR-HOME&page={}"
# wait for page to load
wait = WebDriverWait(driver, 10)

for page in range(1,25): #24pages
    print(f"Scraping page {page} of 24")
    driver.get(BASE_URL.format(page))
    time.sleep(3) # wait for JS to load

    # wait for items to appear
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "items")))

    # find all document items:
    items= driver.find_elements(By.CLASS_NAME, "item")

    for item in items:
        try:
            #document name
            name = item.find_element(By.CLASS_NAME, "doc-title").text.strip()

            #date issued
            date= item.find_element(By.CLASS_NAME,"issued-date").text.strip()
            date.replace("Date issued: ", "")

            # doc type contains brand and type combined
            doc_type_full = item.find_element(By.CLASS_NAME, "doc-type").text.strip()

            #split brand and document type
            if "/" in doc_type_full:
                parts= doc_type_full.split("/")
                brand= parts[0].strip()
                doc_type= parts[1].strip()

            else:
                brand= "Unknown"
                doc_type= doc_type_full

            ws.append([name, brand, doc_type,date])
            print(f"  ✅ {name}")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue

            print(f"Page {page} done.")

# save Excel file
wb.save("laminex_documents.xlsx")
print("Saved to laminex_documents.xlsx")
driver.quit()

