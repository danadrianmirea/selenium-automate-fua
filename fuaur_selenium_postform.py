import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

url = "https://alegerilibere.ro/"
exclude_numbers = ["327003"]

minSleepInterval = 0.1
maxSleepInterval = 0.2

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

def generate_random_phone():
    while True:
        phone = "07" + "".join(str(random.randint(0, 9)) for _ in range(8))
        if not any(exclude in phone for exclude in exclude_numbers):
            return phone

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

def PrintStats(start_time, last_log_time, total_iterations, iterations_in_last_interval, stat_log_time):
    current_time = time.time()
    if current_time - last_log_time >= stat_log_time:
        total_execution_time = current_time - start_time
        print(f"Total execution time: {total_execution_time:.2f} seconds, "
              f"Total number of iterations: {total_iterations}, "
              f"Iterations in the past {stat_log_time} seconds: {iterations_in_last_interval}")
        return current_time, 0  # Reset `last_log_time` and `iterations_in_last_interval`
    return last_log_time, iterations_in_last_interval  # No reset

# Init
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Stat logging variables
stat_log_time = 30
total_iterations = 0
last_log_time = time.time()
start_time = last_log_time
iterations_in_last_interval = 0

print("Starting script")

try:
    while True:        
        # First step
        first_name = random.choice(FirstName)
        last_name = random.choice(LastName)
        full_name = f"{first_name} {last_name}"
        phone = generate_random_phone()

        nume_input = safe_find_element(driver, By.ID, "nume")
        nume_input.clear()
        nume_input.send_keys(full_name)

        phone_input = safe_find_element(driver, By.ID, "phone")
        phone_input.clear()
        phone_input.send_keys(phone)

        continue_button_xpath = "//button[contains(@onclick, 'MultistageForm.CollectAndAdvance')]"
        safe_click(driver, continue_button_xpath)

        #time.sleep(random.uniform(minSleepInterval, maxSleepInterval))

        # Second step
        accept_checkbox = safe_find_element(driver, By.ID, "accept")
        accept_checkbox.click()

        judet_select = Select(safe_find_element(driver, By.NAME, "judet"))
        judet_options = judet_select.options
        random_judet = random.choice(judet_options[1:])
        judet_select.select_by_visible_text(random_judet.text)
        
        uat_select = Select(safe_find_element(driver, By.NAME, "uat"))
        uat_options = uat_select.options
        random_uat = random.choice(uat_options[1:])
        uat_select.select_by_visible_text(random_uat.text)

        localitate_select = Select(safe_find_element(driver, By.NAME, "localitate"))
        localitate_options = localitate_select.options
        random_localitate = random.choice(localitate_options[1:])
        localitate_select.select_by_visible_text(random_localitate.text)

        # Submit form
        sign_button_xpath = "//button[contains(@onclick, 'MultistageForm.CollectAndAdvance')]"
        safe_click(driver, sign_button_xpath)

        print(f"Submitted data for: {full_name}, {phone}, {random_judet.text}, {random_uat.text}, {random_localitate.text}")
        time.sleep(random.uniform(minSleepInterval, maxSleepInterval))

        # Perform cleanup and restart the process
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        driver.get("about:blank")
        driver.get(url)
        
        # Print statistics
        total_iterations += 1
        iterations_in_last_interval += 1
        last_log_time, iterations_in_last_interval = PrintStats(start_time, last_log_time, total_iterations,  iterations_in_last_interval, stat_log_time)


except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
