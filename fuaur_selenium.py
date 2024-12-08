from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import random

# Path to your WebDriver executable (e.g., chromedriver.exe)
driver_path = 'c:/adi/bin/chrome-win64/chromedriver.exe'

# Create a Service object with the path to your WebDriver
service = Service(driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

url = 'https://url.ro/'

try:
    while True:
        # Open the webpage
        driver.get(url)

        # Wait for the element to load (e.g., the <h3> tag with id="counternumber")
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "counternumber"))
            )
            # Extract the number from the element
            number = element.text
            print(f"Extracted number: {number}")
        except Exception as e:
            print(f"Element not found: {e}")

        # Wait for a random time before refreshing
        print(f"Page refreshed at {time.ctime()}")
        time.sleep(random.uniform(1, 3))
finally:
    # Close the browser
    driver.quit()
