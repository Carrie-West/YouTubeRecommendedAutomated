import os
import time
from datetime import datetime
import google_auth_oauthlib
import googleapiclient
import selenium
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from YouTubeCall import scopes, callAPI

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

mail_address = 'dummyAccCV@gmail.com'
password = 'DummyAccount10-'

options = webdriver.ChromeOptions()
options.add_extension("Adblock-für-Youtube™_v5.1.2.crx")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--mute-audio")
driver = webdriver.Chrome(options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = 'https://www.google.com/accounts/Login'
driver.get(url)

driver.get('https://accounts.google.com/servicelogin')
search_form = driver.find_element_by_id("identifierId")
search_form.send_keys(mail_address)
nextButton = driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
nextButton[0].click()

passwordLogin = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, "password")))
passwordElem = driver.find_element_by_css_selector('input[type="password"]')
passwordElem.send_keys(password)
nextButton = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
nextButton[0].click()

start_video = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

callAPI(youtube, "jNQXAC9IVRw")

driver.get(start_video)

try:
    YTLogin = driver.find_element_by_xpath('//*[@id ="button"]')
    wait = WebDriverWait(driver, 2)
    wait.until(EC.element_to_be_clickable((By.NAME, "button")))
    YTLogin.click()
except:
    print("no button")

videos_watched = 0
while videos_watched < 5:
    driver.implicitly_wait(5)
    rec_data = driver.find_element_by_xpath(('.//*[@id="dismissible"]/div/div[1]/a'))
    rec_data = driver.find_element_by_xpath(('.//*[@id="dismissible"]/div/div[1]/a'))


    time_string = driver.find_element_by_class_name("ytp-time-duration").text
    print(time_string)
    video_time = datetime.strptime(time_string, "%M:%S")
    a_timedelta = video_time - datetime(1900, 1, 1)
    video_length = a_timedelta.total_seconds()

    first_rec = rec_data.get_attribute("href")
    callable_address = first_rec[-11:]
    callAPI(youtube, callable_address)

    time.sleep(video_length + 1)
    videos_watched = videos_watched + 1
    driver.get(first_rec)
driver.close()
