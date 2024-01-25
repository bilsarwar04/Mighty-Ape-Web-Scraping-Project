import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bot.constants as const
from selenium.webdriver.common.by import By
from bot.filters import PriceFilter
from bot.report import ReportGenerator
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from tabulate import tabulate 
import numpy as np
import pandas as pd

import time

class WebAutomator:
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(15)
        self.title_list = []
        self.price_list = []
        self.savings_list = []
        self.page_num_list = []
    
    def open_first_page(self):
        self.driver.get(const.BASE_URL)
    
    def close_browser(self):
        self.driver.quit()
    
    def search_item(self, item):
        self.driver.find_element(By.ID, "headerSearchTerm").send_keys(item)
        self.driver.find_element(By.CLASS_NAME, "input-group-btn").click()
    
    def does_product_exist(self, item):
        no_matches_msg = f"Sorry, your search for {item} did not match any items."
        for product in self.get_product_info():
            if product.text == no_matches_msg:
                return False
        return True

    def apply_price_filters(self, min, max):
        filter = PriceFilter(driver=self)
        filter.set_min_price_range(min)
        filter.set_max_price_range(max)
        filter.set_remaining_price_range()
        filter.convert_to_index()
        for indx in filter.get_index_of_selected_prices():
            xpath_reference = f"/html/body/div[2]/div[2]/div/main/nav/div/div/div[3]/div/ul/li[{indx}]/a"
            self.driver.find_element(By.XPATH, xpath_reference).click()
            time.sleep(1)
            
    
    #This method is to make sure we only scrape data from the products section and not from the recommended section
    def get_product_info(self):
        product_element = self.driver.find_elements(By.CLASS_NAME, "products")
        return product_element
    
    def get_title_list(self):
        print(self.title_list)

    def get_price_list(self):
        print(self.price_list)
    
    def get_savings_list(self):
        print(self.savings_list)
    
    def check_for_price_range(self, price, min, max):
        return min <= price <= max
    
    #This method is responsible for finding the title data of products displayed
    def pull_titles(self):
        for product in self.get_product_info():
            title_element = product.find_elements(By.CLASS_NAME, "title")
            for titles in title_element:
                self.title_list.append(titles.text)
        
        
        
    
    #This method is responsible for finding the price data of products displayed
    def pull_prices(self, min, max):
        for product in self.get_product_info():
            dollars = product.find_elements(By.CLASS_NAME, "dollars")
            cents = product.find_elements(By.CLASS_NAME, "cents")
            for dollar, cent in zip(dollars, cents): #Using zip function to iterate through two values simultaneously 
                cent_text = cent.text.replace("\n", "")
                total_price = dollar.text + cent_text 
                if self.check_for_price_range(float(total_price), min, max):
                    self.price_list.append("$" + total_price)
                else:
                    self.price_list.append("false")
        
        
        
    
    
    def pull_savings(self):
        for product in self.get_product_info():
            #Initalising our lists as local variables
            filler = []
            final = []
            pricing_elements = product.find_elements(By.CLASS_NAME, "pricing")
            for price in pricing_elements:
                child_classes = price.find_elements(By.XPATH, "*") #we are finding all child classes of the class 'pricing'
                for child in child_classes:
                    class_name = child.get_attribute("class")
                    filler.append(class_name)
                final.append(filler)
                filler = [] #restarting the filler list so duplicates aren't accounted for
            
        self.create_savings_list(final)
        
    

    def create_savings_list(self, final):
        for product in self.get_product_info():
            saving_element = product.find_elements(By.CLASS_NAME, "saving")
            count = 0
            index = 0
            while index < len(final):
                if "saving" in final[index]:
                    self.savings_list.append(saving_element[count].text)
                    count += 1
                    index += 1
                else:
                    self.savings_list.append("No Deal")
                    index += 1
        


    def find_amount_of_pages(self):
        try:
            pages = self.driver.find_element(By.CLASS_NAME, "pagination")
            all_li = pages.find_elements(By.TAG_NAME, "li")
            for li in all_li:
                if li.text.isdigit():
                    self.page_num_list.append(int(li.text))
        except NoSuchElementException:
            pass

        
    
    
    def proceed_to_next_page(self, min, max):
        self.find_amount_of_pages()
        if self.page_num_list:
            for i in range(self.page_num_list[-1]):
                self.pull_titles()
                self.pull_prices(min, max)
                self.pull_savings()
                try:
                    next_button = self.driver.find_element(By.CLASS_NAME, "icon-more-right")
                    next_button.click()
                    time.sleep(15)
                except NoSuchElementException:
                    pass
        else:
            self.pull_titles()
            self.pull_prices(min, max)
            self.pull_savings()
                
            

    def final_products_list(self):
        valid_indices = [i for i in range(len(self.title_list)) if self.price_list[i] != "false"]
        self.title_list = [self.title_list[i] for i in valid_indices]
        self.price_list = [self.price_list[i] for i in valid_indices]
        self.savings_list = [self.savings_list[i] for i in valid_indices]
        print(self.title_list)
        print(self.price_list)
        print(self.savings_list)
    
    def find_the_best_deal(self):
        best_price_difference = 0
        indices_of_best_deals = []
        
        for i in range(len(self.savings_list)):
            if self.savings_list[i] != "No Deal":
                
                price_difference = float(self.savings_list[i][1:]) - float(self.price_list[i][1:])
                
                if price_difference > best_price_difference:
                    best_price_difference = price_difference
                    indices_of_best_deals.clear()
                    indices_of_best_deals.append(i)
                elif price_difference == best_price_difference:
                    indices_of_best_deals.append(i)
            
        
        if indices_of_best_deals:
            print("The best deals are:")
            for index in indices_of_best_deals:
                print(f"{self.title_list[index]}") 
            print(f"Where you save ${best_price_difference} from the original price.")
        else:
            print("No best deal found.")
            

    def generate_table(self):
        product_dict = {
            "Product Name" : self.title_list,
            "Product Price" : self.price_list,
            "Original Price" : self.savings_list
        }
        data_frame = pd.DataFrame(product_dict)
        print(tabulate(data_frame, headers="keys", tablefmt="fancy_grid", showindex="always"))
        self.find_the_best_deal()

    




    

        
        
