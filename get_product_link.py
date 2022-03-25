from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import datetime

time_now = datetime.datetime.now()

'''opt = webdriver.ChromeOptions()
opt.add_experimental_option("debuggerAddress","localhost:8989")
'''
driver = webdriver.Firefox()
# driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

# Open products page from any category
def open_page(url):
    print('*** Open page ***')
    driver.get(url)
    sleep(1)

# Selenium Page down by ActionChains
def scrollDown(i):
     print('*** Start scrollDown ***')
     while (i != 0 ): 
          try:
               ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
               i -= 1
               print(i)
          except:
               continue

          sleep(5)

     print('*** End scrollDown ***')  
# Get list of products link
def get_links():
     print('*** Start Get links of products ***')
     product_list = driver.find_elements(By.CLASS_NAME,'p-card-wrppr')
     with open('link.txt', 'w') as f:
          for p in product_list:
               link = p.find_element(By.TAG_NAME,'a').get_attribute('href')
               f.write(link + "\n")
          f.close()
     print('*** End Get links of products ***')
               
if __name__ == '__main__':
     # page_urls = ['https://www.trendyol.com/erkek-t-shirt-x-g2-c73','https://www.trendyol.com/elbise-x-c56','https://www.trendyol.com/erkek-spor-ayakkabi-x-g2-c109']
     page_urls = ['https://www.trendyol.com/sr?wc=109650&prc=0-200&pi=7']
     for page_url in page_urls:
          link = page_url + "?prc=0-500"
          open_page(link)
          # To get 1000 product (i = 200) ==> time = 10 min
          i = 10 # products = 216 , time = 2 min
          scrollDown(i)
          get_links()
     print(datetime.datetime.now() - time_now)
