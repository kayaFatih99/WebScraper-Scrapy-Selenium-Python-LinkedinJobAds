import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..items import LinkedinItem
import time

class LinkedinDetailsSpider(scrapy.Spider):
    name = 'linkedin_details'
    allowed_domains = ['www.linkedin.com']
    def start_requests(self):
        url = 'http://quotes.toscrape.com'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = LinkedinItem()

        # Aşağıda input girişleri otonomiyi kolaylaştırmak için eklenmiştir :
        top_link_names = 'berlin_mobile_jobs' # spain_remote_jobs # linklerin txt ismi
        desc_folder_name = 'berlin mobile jobs' # spain remote jobs # klasör(folder) işlem yapmadan önce el ile yapmak gerekir yoksa okumaz.

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        driver.maximize_window()
        
        driver.get("https://www.linkedin.com/login/tr?trk=homepage-basic_intl-segments-login")

        username = driver.find_element(By.XPATH,'//*[@id="username"]')
        username.send_keys('webscrapertest99@gmail.com') # linkedin username or e-mail
        password = driver.find_element(By.XPATH,'//*[@id="password"]')
        password.send_keys('2611563fatih') # linkedin password
        loginButton = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button')
        loginButton.click()
        
        time.sleep(30)
        
        with open(f'output_list/{top_link_names}.txt', 'r',encoding="utf-8") as f:
            data = f.read()
            listem = data.split(",")
        
        txtNumbers = 1
        for job in listem:
            driver.get(job)
            time.sleep(2)
            try:
                job_title = driver.find_element(By.XPATH, '//h1[@class="t-24 t-bold jobs-unified-top-card__job-title"]').text
            except:
                job_title = 'ERR'
            try:
                company_name = driver.find_element(By.XPATH, '//a[@class="ember-view t-black t-normal"]').text
            except:
                company_name = 'ERR'
            try:
                company_linkedin_link = driver.find_element(By.XPATH, '//a[@class="ember-view t-black t-normal"]').get_attribute("href")
            except:
                company_linkedin_link = 'ERR'
            try:
                company_location = driver.find_element(By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-primary-grouping t-black"]/span[@class="jobs-unified-top-card__bullet"]').text
            except:
                company_location = 'ERR'
            try:
                company_image = driver.find_element(By.XPATH, '//img[@class="lazy-image ember-view EntityPhoto-square-3 mb3"]').get_attribute("src")
            except:
                company_image = 'ERR'
            try:
                work_method = driver.find_element(By.XPATH, '//span[@class="jobs-unified-top-card__workplace-type"]').text
            except:
                work_method = 'ERR'
            try:
                post_date = driver.find_element(By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-secondary-grouping t-black--light"]/span[1]').text
            except:
                post_date = 'ERR'
            try:
                applicants = driver.find_element(By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-secondary-grouping t-black--light"]/span[2]/span').text
            except:
                applicants = 'ERR'
            try:
                work_time = driver.find_element(By.XPATH, '//li[@class="jobs-unified-top-card__job-insight"][1]/span').text
            except:
                work_time = 'ERR'

            try:
                driver.find_element(By.XPATH, '//button[@aria-label="Click to see more description"]').click()
                new_str = ''.join(letter for letter in job_title if letter.isalnum())
                job_desc = driver.find_element(By.XPATH, '//div[@id="job-details"]').text
                # Job desc. yazıdırlacağı adres:
                with open(f'output_desc/{desc_folder_name}/{txtNumbers}-{new_str}.txt', 'w',encoding="utf-8") as f:
                    f.write(job_desc)
                txtNumbers = txtNumbers + 1
            except:
                job_desc = "None Description"
                new_str = ''.join(letter for letter in job_title if letter.isalnum())
                # Job desc. yazıdırlacağı adres:
                with open(f'output_desc/{desc_folder_name}/{txtNumbers}-{new_str}.txt', 'w',encoding="utf-8") as f:
                    f.write(job_desc)
                txtNumbers = txtNumbers + 1
            
            items['job_title'] = job_title
            items['company_name'] = company_name
            items['company_linkedin_link'] = company_linkedin_link
            items['company_location'] = company_location
            items['company_image'] = company_image
            items['work_method'] = work_method
            items['post_date'] = post_date
            items['applicants'] = applicants
            items['work_time'] = work_time

            yield items
        
        
        
        