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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("incognito")
     # disable images for chrome
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)
    driver.get(url)

    return driver

def get_discount_data(web_driver) -> list:
    # storage for saved content
    saved_content = []
    time.sleep(5)
    # webdriverwait will wait for a certain class name to appear for 15 seconds 
    try:
        while True:
            # don't be spammy!
            time.sleep(1)
            # connect
            base_column = WebDriverWait(web_driver, 5).until(
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
            WebDriverWait(web_driver, 5).until(
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

def save_content_to_database(saved_content: list):
    connection = sqlite3.connect("content.db")
    cursor = connection.cursor()
    # check if there is a DB and crate it if there isn't
    try:
        cursor.execute("""
                SELECT * FROM discounts
    """)
    except Exception as error:
        print(error)
        print("Error, db  doesn't exist, creating it...")
        cursor.execute("""
                CREATE TABLE discounts (
                    product_name text,
                    new_price real,
                    old_price real,
                    discount text
                )
        """)
        connection.commit()
    
    # save our data
    for single_item in saved_content:
        product_name = single_item[0]
        # only save products with prices
        if single_item[1] == 'Not available': continue
        else: new_price = float(single_item[1][:-2].replace(',', '.').replace(' ', ''))
        if single_item[2] == 'Not available': continue
        else: old_price = float(single_item[2][:-2].replace(',', '.').replace(' ', ''))
        discount = single_item[3]
        
        #some errors may occure, so it's better to use try
        try:
            cursor.execute(f"""
                    INSERT INTO discounts
                    VALUES ('{product_name}', {new_price}, {old_price}, '{discount}')
        """)
        except Exception as error2:
            print(f"Error!\n{error2}")
        connection.commit()

    connection.commit()
    connection.close()
    print("Data is saved!")

def main():
    URL = ''
    with open('url.txt') as file:
        URL = file.read()
    
    driver = start_webdriver(URL)
    saved_content = get_discount_data(driver)
    display_saved_content(saved_content)
    save_content_to_database(saved_content)

# start of the program
if __name__ == "__main__":
    main()
