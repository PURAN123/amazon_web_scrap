import csv
from datetime import datetime
import os
from selenium import webdriver

""" Set chromedriver path """
path = "C:/Users/Puran CD/Downloads/chromedriver"

def amazon_product_details(product_link):
   """ Scrap a website and find all datas """
   amazon_driver = webdriver.Chrome(path)
   amazon_driver.get(product_link)
   """ All values whicih we have to scrap from website """
   product_link=""
   stock= "X"
   author_and_title= ""
   shipping_time= ""
   price=""
   options=[]
   descriptions=""
   categories=""
   country_of_origin=""
   store=""
   image_link=""
   created=""

   try:
      product_link = amazon_driver.current_url
      image_link =  amazon_driver.find_element_by_xpath('//img[@id="landingImage"]').get_attribute('src')
      author_and_title= amazon_driver.find_element_by_xpath('//span[@id="productTitle"]').text
      all_categories = amazon_driver.find_elements_by_xpath('//div[@id="wayfinding-breadcrumbs_feature_div"]/ul/li')
      for category in all_categories:
         categories+= category.text+","
      descriptions = amazon_driver.find_element_by_xpath('//div[@id="productDescription"]').text      
      created = amazon_driver.find_element_by_xpath('//table[@id="productDetails_detailBullets_sections1"]/tbody/tr/td[@class="a-size-base prodDetAttrValue"]').text
      country_of_origin = amazon_driver.find_element_by_xpath('//div[@id="merchant-info"]/span').text
      try:
         store= amazon_driver.find_element_by_xpath('//div[@class="a-section a-spacing-none"]/div/a').get_attribute('href')
      except:
         store= amazon_driver.find_element_by_xpath('//div[@class="a-section a-spacing-none"]/a').get_attribute('href')
      price = amazon_driver.find_element_by_xpath('//span[@class="a-price"]/span/span[@class="a-price-whole"]').text
      shipping_time = amazon_driver.find_element_by_xpath('//div[@id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"]/span/span').text
      stock = ""
      print(product_link, "All details fetched successfully")
   except :
      print(product_link," out of stock")

   """ Write on csv file """
   file_name=f"etsy_output_file-{datetime.now():%Y-%m-%d %H-%m}.csv"
   with open(file_name, 'a', encoding='utf-8') as file_data:
      etsy_product_writer= csv.DictWriter(file_data,fieldnames=[
         'product_link','in_stock','author_and_title','shipping_time','product_price',
         'description','store','created','country_of_origin','image_link','options','categories'
      ])
      if os.stat(file_name).st_size == 0:
         etsy_product_writer.writeheader()
      etsy_product_writer.writerow({
         'product_link':product_link,'in_stock':stock,'author_and_title':author_and_title,'shipping_time':shipping_time,'product_price':price,'description':descriptions,'store':store,'created':created,'country_of_origin':country_of_origin,'image_link':image_link,'options':options,'categories':categories
      })
   amazon_driver.quit()

def main():
   """ Retrieve all product urls and fetch data from each url """
   with open('./amazon_input_file.csv', 'r') as all_product_urls:
      for product_link in all_product_urls:
         amazon_product_details(product_link)
      print("All product's details has been fetched successfully!")
main()