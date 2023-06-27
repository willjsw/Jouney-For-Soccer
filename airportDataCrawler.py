from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

#경기장 최근거리 공항 크롤링 함수
def crawlNearestAirport(stadium):  

    #크롤링 성능 개선 위한 크롬드라이버 옵션 세팅
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--disable-gpu")
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    #크롬드라이버 버전 업데이트 자동화
    chromedriver_autoinstaller.install()  
    
    driver = webdriver.Chrome(options=options)
    #웹페이지 요소 로딩을 위한 대기 시간 설정
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get('https://www.google.com/maps')
        searchPhrase = "Nearest Airport from "+stadium
        searchBox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]')))
        searchBox.send_keys(searchPhrase)
        searchBox.send_keys(Keys.ENTER)
        airportKor = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1')))
        airportLocal = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/h2/span')))
        #결과-> 리스트 형태로 리턴
        return [airportLocal.text,airportKor.text]
    except Exception as e:
        print(e)
        return None
    finally:
        driver.quit()
