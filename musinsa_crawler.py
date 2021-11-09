from crawling import crawl_musinsa_category, categories
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

driver = webdriver.Remote("http://chrome:4444/wd/hub", DesiredCapabilities.CHROME)
# driver = webdriver.Chrome('./chromedriver')
# os.environ['CATEGORY_IDX'] = '0'
# os.environ['START'] = '1'
# os.environ['N'] = '3'
# os.environ['DELAY'] = '5.0'
crawl_musinsa_category(driver, categories[int(os.environ['CATEGORY_IDX'])], int(os.environ['START']), int(os.environ['N']),
                       float(os.environ['DELAY']))
