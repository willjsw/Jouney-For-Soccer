from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

def crawlNearestAirport(stadium):  

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--disable-gpu")
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    chromedriver_autoinstaller.install()  
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get('https://www.google.com/maps')
        searchPhrase = "Nearest Airport from "+stadium
        searchBox = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        searchBox.send_keys(searchPhrase)
        searchBox.send_keys(Keys.ENTER)
        airport = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/h2/span')))
        return airport.text
    except Exception as e:
        print("크롤링 실패")
        return None
    finally:
        driver.quit()
