import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class Search_By_Keyword_without_sharafdgonly:
# initialize the web driver


    def UploadFileOnGoogleDrive(self,file_path):
        # Replace the values in the following variables with your own.
        FILE_PATH = file_path
        FOLDER_ID = '1AoTVCUt-Pb0Y2LYSMzq0_8uiFTZIqcjC'

        # Create credentials object from JSON file.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = 'creds/cred.json'
        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Create Drive API client.
        service = build('drive', 'v3', credentials=creds)

        # Create file metadata.
        file_metadata = {'name': os.path.basename(FILE_PATH), 'parents': [FOLDER_ID]}

        # Create media object.
        media = MediaFileUpload(FILE_PATH, resumable=True)

        # Upload file.
        try:
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'File ID: {file.get("id")}')
        except HttpError as error:
            print(f'An error occurred: {error}')
            file = None




    def fetch_pdp(self,driver, url,check_once):
            model_id = ""
            sku = ""
            total_images = 0
            rating = 0
            review = 0
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                # driver.set_page_load_timeout(30)
                try:
                    ids = driver.find_element(By.XPATH,"//meta[@itemprop='mpn']")
                    model_id = ids.get_attribute("content")
                except:
                    # driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                
                try:
                    sku_ids = driver.find_element(By.XPATH,"//meta[@itemprop='sku']")
                    sku = sku_ids.get_attribute("content")
                except:
                    # driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    sku = ""
                
                    rating = 0
                review = 0
                try:
                    rating_div = driver.find_element(By.CSS_SELECTOR,".ms-1.product-rating-count.fw-600")
                    rating=float(rating_div.text)
                    # rating_span = rating_div.find_element(By.TAG_NAME,"span")
                    # rating = float(rating_span.text)
                    review_div = driver.find_element(By.CSS_SELECTOR,".review-details.reviewCount.ms-2")
                    # review_span = review_div.find_element(By.TAG_NAME,"span")
                    # review = float(review_span.text)
                    num = re.findall(r'\d+', review_div.text) 
                    review=num[0]
                except:
                    rating = 0
                    review = 0
                try:
                    list_of_images = set()
                    images_list_container = driver.find_element(By.CLASS_NAME,"no_video")
                    list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                    for imag in list_of_img_tags:
                        list_of_images.add(imag.get_attribute("src"))
                
                    total_images = len(list_of_images)  
                    pass
                except:
                    driver.switch_to.window(driver.window_handles[0])
                    total_images=0

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,sku,total_images,rating,review
            except:
                return model_id,sku,total_images,rating,review
    # navigate to a website

    def extract_data_by_keyword(self,driver, url,cat_name,search_keyword,check_once):
        # url = "https://uae.sharafdg.com/?q=Air%20Purifier&post_type=product"
        driver.get(url)
        try:
            ids = driver.find_element(By.ID,"hits")
        except:
            return False
        all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")

        all_data = []
        count =1
        for div in all_divs:
        # get all elements with the tag "a"
            title = div.find_element(By.TAG_NAME,"h4")
            # print(title.text)
            link = div.find_element(By.TAG_NAME,"a")
            img = div.find_element(By.TAG_NAME,"img")
            price = div.find_element(By.CSS_SELECTOR,".price")
            if title.text.find('Samsung') != -1 or title.text.find("LG") != -1 or title.text.find("Dyson") != -1:
                title_name = title.text
                price_ = price.text,
                image_url = img.get_attribute("src")
                img_link = link.get_attribute("href")
                full_title_arr = title.text.split()
                brand_name = full_title_arr[0]
                
                mpn,sku,total_images,rating,review = self.fetch_pdp(driver,link.get_attribute("href"),check_once)
                check_once+=1    
                data = {
                    "Date": datetime.today(),
                    "Region": "MEA",
                    "Country": "UAE",
                    "Retailer": "Sharafdg",
                    "category":  cat_name,
                    "keyword": search_keyword,
                    "brand": brand_name,
                    "Rank": count,
                    "mpn": mpn,
                    "sku": sku,
                    "title":title_name,
                    "link": img_link,
                    "price":price_,
                    "image url":image_url,
                }
        
                all_data.append(data)
            count+=1
            
        # print(all_data)

        # close the web driver


        df = pd.DataFrame(all_data)
        # print(df)
        return df


    def __init__(self):
        driver = webdriver.Chrome()
        # -------------------------------------------------------------------------------------
        # For Search Keywords
        # Reading the excel sheet
        df = pd.read_excel("Sharaf_Dg/search_keywords/by_search_keywords.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []
        list_of_keywords = []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['keywords']:
            list_of_keywords.append(dt)
            testing_url = f"https://uae.sharafdg.com/?q={dt}&post_type=product"
            list_of_urls.append(testing_url)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()

        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0

        while i < len(list_of_urls):

            
            # storing the extracted data in df to be used in future
            rtnData=self.extract_data_by_keyword(driver,list_of_urls[i],list_of_categories[i],list_of_keywords[i],check_once)
            if type(rtnData) == bool:
                pass
            else:
            # appending the extracted data in the empty dataframe 
                dataframe_final = pd.concat([dataframe_final,rtnData])
                # dataframe_final.append(df)
                
                # printing dataframe final to show that the data is storing perfectly 
                # print(dataframe_final) 

                # Printing completed to show that the urls are fetching the data 
                print("completed")
                i+=1
            check_once+=1
        # Closing the browser 
        driver.quit()

        # Printing the dataframe with all the data 
        print(dataframe_final)

        # Storing the dataframe in the text.xlsx file 
        # dataframe_final.to_excel(excel_writer = "output/search_by_keyword_without_sharafdgonly.xlsx")




        dataframe_final.to_excel(excel_writer = f"Sharaf_Dg/output/{datetime.today().date()}_search_by_keyword_without_sharafdgonly.xlsx")
        file_path = f"Sharaf_Dg/output/{datetime.today().date()}_search_by_keyword_without_sharafdgonly.xlsx"



        self.UploadFileOnGoogleDrive(file_path)