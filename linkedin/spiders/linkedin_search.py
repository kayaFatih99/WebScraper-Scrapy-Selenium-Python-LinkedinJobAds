import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class LinkedinSearchSpider(scrapy.Spider):
    name = 'linkedin_search'
    allowed_domains = ['www.linkedin.com']

    def start_requests(self):
        url = 'http://quotes.toscrape.com'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        search_keywords = 'mobile developer' # full stack developer 
        search_location = 'London' # Madrid, Spain
        search_filter = '&f_AL=true' # remote filters => &f_WT=2
        top_link_names = 'london_mobile_jobs' # spain_remote_jobs # linklerin txt ismi

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        driver.maximize_window()
        
        driver.get("https://www.linkedin.com/login/tr?trk=homepage-basic_intl-segments-login")

        username = driver.find_element(By.XPATH,'//*[@id="username"]')
        username.send_keys('') # linkedin username or e-mail
        password = driver.find_element(By.XPATH,'//*[@id="password"]')
        password.send_keys('') # linkedin password
        loginButton = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button')
        loginButton.click()
        
        time.sleep(30) 
        
        driver.get("https://www.linkedin.com/jobs/search/")

        search = driver.find_element(By.XPATH, '//input[@class="jobs-search-box__text-input jobs-search-box__keyboard-text-input"]')
        search.send_keys(search_keywords)
        city = driver.find_element(By.XPATH,'//input[@class="jobs-search-box__text-input"]')
        city.clear()
        city.send_keys(search_location) 
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        time.sleep(10)

        getUrl = driver.current_url
        fullUrl = getUrl + search_filter 
        driver.get(fullUrl)

        isNextDisabled = False
        iNumber = 1
        while not isNextDisabled:
            blocks = driver.find_elements(By.XPATH,'//ul[@class="scaffold-layout__list-container"]/li')
            
            for block in blocks:
                link = block.find_element(By.XPATH, './/div/div[1]/div[1]/div[1]/a').get_attribute("href")
                # Toplanan linklerin yazdırılacak adresi :
                with open(f'output_list/{top_link_names}.txt', 'a',encoding="utf-8") as f:
                    f.write(link + " , ")
                driver.execute_script("arguments[0].scrollIntoView();", block)

            iNumber = iNumber + 1
            iNumberSayac = driver.find_element(By.XPATH,'//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]/li[last()]/button/span').text
            
            try:
                nextPage = driver.find_element(By.XPATH,f'//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]/li[@data-test-pagination-page-btn="{iNumber}"]/button')
            except:
                nextPage = driver.find_element(By.XPATH,'//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]/li[not(@data-test-pagination-page-btn)][last()]/button')
                    
            if iNumber > int(iNumberSayac):
                isNextDisabled = True
                print(f"Sayaç çalıştı :) => {iNumberSayac}")
            else:
                nextPage.click()
                WebDriverWait(driver, 10)
        
            



