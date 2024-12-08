import requests
import time
import random

url = 'url'

while True:
    try:
        response = requests.get(url)
        # print(response.text)
        print(f"Page refreshed at {time.ctime()}")
        if "error" in response.text:
            print("error")
        time.sleep(random.uniform(0.5, 1))
    except Exception as e:
        print(f"An error occurred: {e}")
        break
