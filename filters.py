class PriceFilter:
    def __init__(self, driver):
        self.driver = driver
        self.selected_prices = []
        self.index_of_selected_prices = []
        self.price_ranges = [[1, 10], [10, 20], [20, 40], [40, 60], [60, 80], [80, 100], [100, 150],
                    [150, 200], [200, 500], [500, 1000], [1000, 2000], [2000, 1000000]]
    
    
    def get_price_ranges(self):
        return self.price_ranges
    
    def get_selected_prices(self):
        return self.selected_prices
    
    def get_selected_prices_length(self):
        return len(self.selected_prices)
    
    def get_index_of_selected_prices(self):
        return self.index_of_selected_prices
    
    def get_length_of_index_of_selected_prices(self):
        return len(self.index_of_selected_prices)
    
    def set_min_price_range(self, min):
        for price in self.price_ranges:
            if min in range(price[0], price[1]):
                self.selected_prices.append(price)
        
        return self.selected_prices
    
    def set_max_price_range(self, max):
        for price in self.price_ranges:
            if (max - 1) in range(price[0], price[1]):
                if price not in self.selected_prices:
                    self.selected_prices.append(price)

        return self.selected_prices
    
    def set_remaining_price_range(self):
        if len(self.selected_prices) == 2:
            index_of_min = self.price_ranges.index(self.selected_prices[0])
            index_of_max = self.price_ranges.index(self.selected_prices[1])
            first_element = self.selected_prices[0]
            last_element = self.selected_prices[1]
            self.selected_prices.remove(first_element)
            self.selected_prices.pop()
            for price in range(index_of_min + 1, index_of_max):
                self.selected_prices.append(self.price_ranges[price])
            self.selected_prices.insert(0, first_element)
            self.selected_prices.append(last_element)
            return self.selected_prices
        else:
            return self.selected_prices
    
    ''''
    The purpose of the method below is to convert the given price ranges to it's appropiate index when the bot begins to 
    choose the appropiate boxes to filter the price by.
    While we could have just done this from the beginning, I wanted to implement the other methods as it made it 
    easier to visualise the code properly and do appropiate unit testing of the methods
    '''
    def convert_to_index(self):
        for i in range(0, len(self.selected_prices)):
            index_of_ele = self.price_ranges.index(self.selected_prices[i])
            self.index_of_selected_prices.append(index_of_ele + 1)
        
        return self.index_of_selected_prices
    
    

        


        
    
    
            
        
