import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://anki-decks.com/deck/create_deck_general_knowledge/"

#get user agent
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://httpbin.org/headers")
userAgent = driver.execute_script("return navigator.userAgent;")

#get csrf token
session = requests.Session()
response = session.get(url)
soup = bs(response.text, "html.parser")
csrfInput = soup.find("input", {"name": "csrfmiddlewaretoken"})
csrfToken = csrfInput["value"] if csrfInput else None

#send post request
session.headers.update({
    "Referer": "https://anki-decks.com/deck/create_deck_general_knowledge/",
    "User-agent": userAgent
})

data = {
    "text": "The mitochondria is the powerhouse of the cell.",
    "csrfmiddlewaretoken": csrfToken
}

response = session.get(url)
print(response.status_code, response.text)

# import time

# service = Service(executable_path="Python stuff\\transcriptMaker\\chromedriver.exe")
# driver = webdriver.Chrome(service=service)
# driver.get("https://google.com")

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
# )

# inputEl = driver.find_element(By.CLASS_NAME, "gLFyf")
# inputEl.send_keys("hello there" + Keys.ENTER)

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Tech With Tim"))
# )

# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech With Tim")
# link.click()

# time.sleep(10)

# driver.quit()