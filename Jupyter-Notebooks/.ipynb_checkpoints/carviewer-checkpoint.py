from IPython.display import HTML, display
import pandas as pd
import numpy as np

# Webscraping libraries
from urllib.request import urlopen # url inspector
from bs4 import BeautifulSoup
import re



def car_viewer():
    
    input_body = input("What body type of car do you want to view? ")
    bodystyle = str(input_body)
    
    
    input_brand = input("What brand do you want to view? ")
    brand= str(input_brand.title().replace(" ", "-"))

    input_pages = input("What page do you want to view? ")
    pages = int(input_pages)
    
    my_url = 'https://www.autovillage.co.uk/used-car/{}/page/{}/filter/bodystyle/{}'.format(brand, pages, bodystyle)

    
    my_client = urlopen(my_url) # open up a connection to the webpage
    image_viewer =my_client.read() # reads all the html from the webpage
    
    image_soup = BeautifulSoup(image_viewer, "html.parser")
    container_image = image_soup.findAll("div", {"class":"ucatid20"})
    
    for item in range(0,len(container_image)):
        cars = display(HTML(str(container_image[item].findAll("div", {"class":"mb5"})[0].img)))
    
    return cars

if __name__ == '__main__':
    car_viewer()