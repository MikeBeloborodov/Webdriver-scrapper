from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

def start_webdriver(url: str):
    # options 
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("incognito")
    # disable images for chrome
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options, chrome_options=chrome_options)
    driver.get(url)

    return driver

def get_discount_data(web_driver) -> list:
    # storage for saved content
    saved_content = []

    # webdriverwait will wait for a certain class name to appear for 15 seconds 
    try:
        while True:
            # don't be spammy!
            time.sleep(3)
            # connect
            base_column = WebDriverWait(web_driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "p-retailer__base-column"))
            )
            price_boxes = base_column.find_elements_by_class_name("b-offer__root")

            #save data
            for box in price_boxes:
                # sometimes there is no data and program will stop with an error
                # so to avoid it just put these statements in try except
                # it doesn't matter to me if there is no data
                try: description = box.find_element(By.CLASS_NAME, "b-offer__description").text
                except: description = "No description"

                try: new_price = box.find_element(By.CLASS_NAME, "b-offer__price-new").text
                except: new_price = "Not available"

                try: old_price = box.find_element(By.CLASS_NAME, "b-offer__price-old").text
                except:old_price = "Not available"

                try: discount = box.find_element(By.CLASS_NAME, "b-offer__badge").text
                except: discount = "Not available"

                saved_content.append([
                    description, 
                    new_price,
                    old_price,
                    discount,
                ])

            # find load more button
            load_more_button = ""
            WebDriverWait(web_driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "b-button__content"))
            )
            buttons = web_driver.find_elements(By.CLASS_NAME, "b-button__content")
            for button in buttons:
                if button.text == "Вперед →":
                    load_more_button = button
            # exit loop if no more data
            if not load_more_button:
                # close browser
                print("End of data")
                web_driver.quit()
                return saved_content
            else:
                load_more_button.click()
            
            # sleep for a little bit on every page
            # don't spam

    except Exception as error:
        print("ERROR!")
        print(error)
        web_driver.quit()
        return saved_content

def display_saved_content(saved_content: list):
    for content in saved_content:
        print(f"Name: {content[0]}")
        print(f"New price: {content[1]}")
        print(f"Old price: {content[2]}")
        print(f"Dicount: {content[3]}")

def main():
    URL = "https://edadeal.ru/moskva/retailers/5ka"

    driver = start_webdriver(URL)
    saved_content = get_discount_data(driver)
    display_saved_content(saved_content)


if __name__ == "__main__":
    main()