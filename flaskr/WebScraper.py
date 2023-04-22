from bs4 import BeautifulSoup
from flask import Flask, flash, request, redirect, url_for, session, render_template
import requests

class weapon_scraper:
    
        
    def __init__(self):
        #price of item on megastore
        self.craze_price = 0

        #price of item on Anime Wire
        self.AliExpress_Price = 0

        self.Craze_item = 'https://www.crazecosplay.com/products/assassination-classroom-ansatsu-kyoshitsu-nagisa-shiota-karma-akabane-cosplay-weapon?variant=42184692793563&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfAwrE4q1f3KnlkpO-E0-WuBVQgvy-7ypYKsKETu6C9YbHDm_Sz_-SBIvRY'
        self.AliExpress_item = 'https://s.click.aliexpress.com/deep_link.htm?aff_short_key=UneMJZVf&dl_target_url=https%3A%2F%2Fwww.aliexpress.com%2Fitem%2F3256805160010822.html%3F_randl_currency%3DUSD%26_randl_shipto%3DUS%26src%3Dgoogle'
        
    def craze(self):

        # Send a request to the given URL and get the HTML content
        response = requests.get(self.Craze_item)
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the price element by its class name
        price_element = soup.find('span', {'class': 'price-item price-item--regular'})

        # Extract the price from the price element
        self.craze_price = price_element.text.strip()

        return int(self.craze_price)
        

    def ali_Express(self):
        
        response = requests.get(self.AliExpress_item)
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the price element by its class name
        price_element = soup.find('span', {'class': 'product-price-value'})

        # Extract the price from the price element
        self.AliExpress_Price = price_element.text.strip()

        return int(self.AliExpress_Price)



    def compare(self):

        if self.AliExpress_Price< self.craze_price:
            return self.AliExpress_Price

        elif self.AliExpress_Price > self.craze_price:
            return self.Craze_item

        elif self.craze_price == self.AliExpress_Price:
            return self.Craze_item
