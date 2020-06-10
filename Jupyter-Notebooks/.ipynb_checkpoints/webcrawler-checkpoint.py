
#===========================================================================================#
# Imports                                                                                   #
#===========================================================================================#

import pandas as pd
import numpy as np

# Webscraping libraries
from urllib.request import urlopen # url inspector
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

#===========================================================================================#
# Functions                                                                                 #
#===========================================================================================#

def autovillage_crawler(): # web_crawler version 1.1 accepts lists for car brands
    
        print("""
     Auto Village Webscraper! - Version 1.1
    
     A car web scraping program created by Paul Aleksis Williams.
    
     Program description:
    
    
     This programs scrapes cars listed on the autovillage.co.uk website, cleans the
     entries, drops duplicated entries, drops entries with missing values, and
     returns a data frame that contains 1 target variable and 8 features.
    
    
     Program inputs:
    
     1. Input a car manufacturer name or leave blank for all manufacturers.
        please use a hyphen for names with spaces (mercedes-benz)
    
     2. Input the body style of cars you want to scrape ot leave empty for all.
       options: saloon, hatchback, 4x4, estate, coupe, convertible, mpv. For
       multiple styles seperate input with a comma.
    
     3. Input the number of pages to scrape there are 10 cars per page. If left
       blank, it will scrape 1 page per body style.
    
     4. Input a name for the file to save it as a csv in the current directory.
       If left blank, It will not save but you can set it as a variable to view
       the table.
       
       
     Program output:
    
    
     The function returns a cleaned data frame of cars scraped from autovillage.co.uk
     dropping all the missing values within the websites interface, and removing any
     duplicated cars.
    
    
     Program save feature:
    
    
     You can leave the save input empty and the file will not be saved.
    
     You can set a variable for this function in jupyter notebooks and manipulate
     the created pandas object as normal.
    
    
    
    """)
    
    # Features
        price =[] # car price
        year_make_model =[] # year made, brand name, model
        eng_tran =[] # engine size and transmission type
        door_body =[] # number of doors and body style
        mileage =[] # number of miles on the odometer

        # body style available inputs
        all_styles = ["saloon", "hatchback", "4x4", "estate", "coupe", "convertible", "mpv"]

        # take user input of body style. If left blank all body inputs will be taken
        print("\n")
        print("Inputs:")
        print("------------------------------------------------------------------------------------------------------")

        input_brand = input("Enter a car brand you are interested in (leave blank for all): ")
        car_brand = input_brand.lower().replace(",", "")
        if car_brand == "":
            brands = " "
        else:
            brands = list(car_brand.split())
        

        input_body = input("Enter a body style (or leave blank for all): ")
        body = input_body.lower().replace(",", "")

        if  body=="":
            bodystyle = all_styles
        else: 
            bodystyle = list(body.split())


        # amount of pages input
        input_pages = input("Enter the amount of pages you want to scrape (or leave blank for 1): ")

        if input_pages =="":
            pages= [1]
        else:
            pages = range(1, int(input_pages)+1)

       

        #progress bar info
        predicted_count = len(pages)*10*len(bodystyle)*len(brands)
        print("\n")
        print("ETA of process:")
        print("------------------------------------------------------------------------------------------------------")
        print("{} cycles of {} pages:".format(len(bodystyle), len(pages)))
        print("Expecting: ~ {} cars".format(predicted_count))

        for p in bodystyle:
            for i in tqdm(pages):
                for car_brand in brands:
                    if brands == " ":
                        url= 'https://www.autovillage.co.uk/used-car/page/{}/filter/bodystyle/{}'.format(i, p)
                    else:
                        url= 'https://www.autovillage.co.uk/used-car/{}/page/{}/filter/bodystyle/{}'.format(car_brand, i, p)
                
                    html= urlopen(url)
                    autovillage_page= html.read()
                    soup= BeautifulSoup(autovillage_page, "html.parser")

                    # parsed into the container that holds information about the cars
                    container= soup.findAll("div", {"class":"ucatid20"})
                    # parsed to be price only
                    container2= soup.findAll("div", {"class":"avprice"})
                    x = len(container)

                    for item in container2:

                        # only loop based on iterations from the length of container1 not container 2 to avoid missmatch on lists
                        if x > 0:
                            x -= 1

                            if item == None:
                                price.append("")
                            else:
                                price.append(item.text)


                    for item in range(0, len(container)):

                        #year, make, and model
                        car_names= container[item].div.findAll("div", {"class":"item"})[0]                
                        # debug nulls
                        if car_names == None:
                            year_make_model.append("")
                        else:
                            year_make_model.append(car_names.get_text().strip())


                        #engine size and transmission type
                        tran = container[item].div.span
                        # debug nulls for engine and transmission
                        if tran == None:
                            eng_tran.append("")
                        else:
                            eng_tran.append(tran.get_text())

                        # number of doors and car body type
                        door_bod = container[item].div.findAll("div", {"class":"item"})[2].span
                        # debug nulls
                        if door_bod == None:
                            door_body.append("")
                        else:
                            door_body.append(door_bod.get_text())

                        # Car mileage
                        car_mileage = container[item].div.findAll("div", {"class":"item"})[3].span 
                        # fix null objects where certain features were not entered
                        if car_mileage is None:
                            mileage.append("")
                        else:
                            for item in car_mileage:
                                   mileage.append(item)
                    # make the df
            df = pd.DataFrame({'price':price, 
                               'mileage':mileage, 
                               'door/body':door_body, 
                               'eng/tran':eng_tran, 
                               'year/make/model':year_make_model})        

        # clean the df
        # remove my pound signs and commas from the price column

        df['price'] = df['price'].str.replace("£|,","")

        # remove span html flags from mileage

        df['mileage'] = df['mileage'].str.replace("miles|,", "")


        # remove door from door/body
        df['door/body'] = df['door/body'].str.replace("Door", "")

        # remove cc from eng (may convert this to litres later)
        df['eng/tran'] = df['eng/tran'].str.replace("cc", "")

        # remove class from mercedes so that it can follow a year-model-class format like the other cars do
        df['year/make/model'] = df['year/make/model'].str.replace("Class", "")
        df['year/make/model'] = df['year/make/model'].str.replace("Land Rover", "Land-Rover")
        df['year/make/model'] = df['year/make/model'].str.replace("Range Rover Sport", "Range-Rover-Sport")
        df['year/make/model'] = df['year/make/model'].str.replace("Discovery Sport", "Discovery-Sport")
        df['year/make/model'] = df['year/make/model'].str.replace("Aston Martin", "Aston-Martin")
        df['year/make/model'] = df['year/make/model'].str.replace("Alfa Romeo", "Alfa-Romeo")
        df['year/make/model'] = df['year/make/model'].str.replace("Corvette", "Chevrolet")
        df['year/make/model'] = df['year/make/model'].str.replace("C7", "Corvette-C7")
        # split door count and body style

        df[['door_count','body_style']]= df['door/body'].str.split(expand=True)

        # split engine size and transmission

        df[['engine_size(cc)', 'transmission']] = df['eng/tran'].str.split(expand=True)

        # split year , make, and model into seperate columns

        df['year'] = df['year/make/model'].str.split(' ', expand=True)[0]
        df['brand'] = df['year/make/model'].str.split(' ', expand=True)[1]
        df['model'] = df['year/make/model'].str.split(' ', expand=True)[2]

        # drop the labels that were split and rename the old ones to include measurement unit
        df.drop(labels=['door/body','eng/tran', 'year/make/model'], axis=1, inplace=True)
        df.rename(columns={"mileage": "mileage(mi)", "price":"price(£)"}, inplace=True)

        # convert strings to integers
        df['price(£)'] = pd.to_numeric(df['price(£)'], errors='coerce')
        df['mileage(mi)'] = pd.to_numeric(df['mileage(mi)'], errors='coerce')
        df['door_count'] = pd.to_numeric(df['door_count'], errors='coerce')
        df['engine_size(cc)'] = pd.to_numeric(df['engine_size(cc)'], errors='coerce')
        df['year'] = pd.to_numeric(df['year'], errors='coerce')


        # Drop nulls
        df.dropna(axis=0, inplace=True)


        # Drop duplicates
        df.drop_duplicates(keep='first', inplace=True)

        # Count how many cars got scraped
        actual_count = len(df)
        print("\n")
        print("Output:")
        print("------------------------------------------------------------------------------------------------------")
        print("Done! you scraped: ", len(df), "cars!")
        print("{} cars were dropped due to poor format".format(predicted_count - actual_count))

        # Create the save with user defined name. If left blank the save wont happen
        input_save = input("Name to save file as (leave blank to not save): ")
        save_file_name = str(input_save)

        print("------------------------------------------------------------------------------------------------------")
        if save_file_name == "":
            print("File Not Saved!")
        else:
            file_path = save_file_name+".csv"
            print("File saved as {}".format(save_file_name+".csv"), "in the current directory!")
            result = df.to_csv(file_path)



        return df

#===========================================================================================#

if __name__ == '__main__':
    autovillage_crawler()
