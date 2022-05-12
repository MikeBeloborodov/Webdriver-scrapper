from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_webdriver(url: str):
    # options 
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("incognito")

    # driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    return driver

def get_discount_data(web_driver) -> list:
    # storage for saved content
    saved_content = []

    try:
        base_column = WebDriverWait(web_driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "p-retailer__base-column"))
        )
        price_boxes = base_column.find_elements_by_class_name("b-offer__root")
        for box in price_boxes:
            saved_content.append([
                box.find_element(By.CLASS_NAME, "b-offer__description").text, 
                box.find_element(By.CLASS_NAME, "b-offer__price-new").text,
                box.find_element(By.CLASS_NAME, "b-offer__price-old").text,
                box.find_element(By.CLASS_NAME, "b-offer__badge").text,
            ])
    finally:
        # close browser
        web_driver.quit()

    return saved_content

def display_saved_content(saved_content: list):
    for content in saved_content:
        print(f"Name: {content[0]}")
        print(f"New price: {content[1]}")
        print(f"Old price: {content[2]}")
        print(f"Dicount: {content[3]}")

def main():
    URL = ""

    driver = start_webdriver(URL)
    saved_content = get_discount_data(driver)
    display_saved_content(saved_content)

if __name__ == "__main__":
    main()