import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bot.constants as const
from selenium.webdriver.common.by import By

class ReportGenerator:
    def __init__(self, driver):
        self.driver = driver
    
    def convert_to_savings(self, price_list, savings_list):
        self.price_list = price_list
        self.savings_list = savings_list
        length = len(self.savings_list)
        for i in range(length):
            price = float(self.savings_list[i].replace("$", ""))
            saving = float(self.savings_list[i].replace("$", ""))
            saving[i] = price - saving
    
    def filter_to_min_and_max(self, product_dict):
        self.product_dict = product_dict