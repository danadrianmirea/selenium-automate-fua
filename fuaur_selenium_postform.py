import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://alegerilibere.ro/"
exclude_numbers = ["327003"]

# Arrays of Romanian names
FirstName = [
    "Andrei", "Mihai", "Ion", "Cristian", "Alexandru", "Gabriel", "Vlad", "Daniel", "Ștefan", "Florin",
    "Maria", "Ioana", "Elena", "Ana", "Gabriela", "Alina", "Diana", "Monica", "Adriana", "Raluca",
    "George", "Cătălin", "Răzvan", "Paul", "Lucian", "Victor", "Tiberiu", "Adrian", "Sergiu", "Iulian",
    "Silviu", "Liviu", "Valentin", "Cosmin", "Dragoș", "Eugen", "Claudiu", "Nicolae", "Ovidiu", "Marian",
    "Cristina", "Simona", "Anca", "Liliana", "Roxana", "Carmen", "Irina", "Claudia", "Mirela", "Oana",
    "Teodora", "Bianca", "Alexandra", "Georgiana", "Andreea", "Loredana", "Violeta", "Ramona", "Daniela", "Doina",
    "Sofia", "Ema", "Aurelia", "Sabina", "Elisabeta", "Anastasia", "Natalia", "Camelia", "Lavinia", "Ecaterina",
    "Nicoleta", "Felicia", "Ioan", "Costin", "Teodor", "Petru", "Traian", "Grigore", "Mircea", "Vasile",
    "Cornel", "Constantin", "Virgil", "Florentin", "Laurențiu", "Anton", "Șerban", "Viorel", "Sorin", "Bogdan"
]

LastName = [
    "Popescu", "Ionescu", "Georgescu", "Dumitrescu", "Stan", "Radu", "Diaconu", "Marin", "Gheorghe", "Tudor",
    "Stoica", "Nistor", "Petrescu", "Barbu", "Ilie", "Lungu", "Cojocaru", "Dragomir", "Chirila", "Costache",
    "Munteanu", "Călin", "Popa", "Savu", "Negrea", "Enache", "Badea", "Ciobanu", "Roman", "Constantinescu",
    "Ciucu", "Dima", "Varga", "Matei", "Bratu", "Zamfir", "Panait", "Neagu", "Cristea", "Grigorescu",
    "Voinea", "Dobre", "Balint", "Filip", "Mihăescu", "Anghel", "Mazilu", "Sandu", "Ștefănescu", "Rusu",
    "Pavel", "Moraru", "Țiganu", "Banu", "Ghiță", "Prunaru", "Șerban", "Oprea", "Moisescu", "Bălan",
    "Savulescu", "Neacșu", "Fieraru", "Lazăr", "Olteanu", "Călinescu", "Manole", "Iftimie", "Hoinaru", "Tănase",
    "Florea", "Dăscălescu", "Cârciumaru", "Ciubotaru", "Stroe", "Grama", "Stanciu", "Voinescu", "Toma", "Ganea",
    "Bărbulescu", "Petrică", "Tudose", "Manea", "Șoarec", "Pașcu", "Chirilă", "Săvescu", "Mitrea", "Borcea"
]

# Function to generate random phone numbers
def generate_random_phone():
    while True:
        phone = "07" + "".join(str(random.randint(0, 9)) for _ in range(8))
        # Check if any excluded number is in the generated phone
        if not any(exclude in phone for exclude in exclude_numbers):
            return phone

# Function to safely interact with elements
def safe_click(driver, xpath):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
    except Exception as e:
        print(f"Error clicking element with XPath {xpath}: {e}")
        try:
            element = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", element)
        except Exception as js_e:
            print(f"JavaScript click failed for XPath {xpath}: {js_e}")

def safe_find_element(driver, by, value):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.presence_of_element_located((by, value)))

# Start Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the path to your ChromeDriver if necessary
driver.get(url)

try:
    while True:
        # First step
        first_name = random.choice(FirstName)
        last_name = random.choice(LastName)
        full_name = f"{first_name} {last_name}"
        phone = generate_random_phone()

        # Fill "nume"
        nume_input = safe_find_element(driver, By.ID, "nume")
        nume_input.clear()
        nume_input.send_keys(full_name)

        # Fill "phone"
        phone_input = safe_find_element(driver, By.ID, "phone")
        phone_input.clear()
        phone_input.send_keys(phone)

        # Click the "Continuă" button
        continue_button_xpath = "//button[contains(@onclick, 'MultistageForm.CollectAndAdvance')]"
        safe_click(driver, continue_button_xpath)

        # Wait for the second step to load
        time.sleep(random.uniform(1, 3))

        # Second step
        accept_checkbox = safe_find_element(driver, By.ID, "accept")
        accept_checkbox.click()

        # Select random "judet"
        judet_select = Select(safe_find_element(driver, By.NAME, "judet"))
        judet_options = judet_select.options
        random_judet = random.choice(judet_options[1:])  # Exclude the first placeholder option
        judet_select.select_by_visible_text(random_judet.text)

        # Select random "uat"
        uat_select = Select(safe_find_element(driver, By.NAME, "uat"))
        uat_options = uat_select.options
        random_uat = random.choice(uat_options[1:])  # Exclude the first placeholder option
        uat_select.select_by_visible_text(random_uat.text)        

        # Select random "localitate"
        localitate_select = Select(safe_find_element(driver, By.NAME, "localitate"))
        localitate_options = localitate_select.options
        random_localitate = random.choice(localitate_options[1:])  # Exclude the first placeholder option
        localitate_select.select_by_visible_text(random_localitate.text)

        # Click the "Semnează" button
        sign_button_xpath = "//button[contains(@onclick, 'MultistageForm.CollectAndAdvance')]"
        safe_click(driver, sign_button_xpath)

        # Wait for a random time between 1s and 3s
        time.sleep(random.uniform(1, 3))

        # Restart the process
        driver.get(url)
        time.sleep(random.uniform(1, 3))

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
