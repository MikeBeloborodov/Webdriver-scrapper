from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = ""

# options 
options = Options()
options.add_argument("start-maximized")
options.add_argument("incognito")

# driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)

# close browser
driver.quit()
